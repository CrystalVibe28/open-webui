"""Apply identity privacy to JSON APIs, inside response compression.

Directory filtering/authorization happens in the routes before pagination. This
last serialization boundary also covers embedded owners on shared resources and
old message/reaction payloads. It does not buffer SSE, files or websocket frames.
"""

from fastapi import HTTPException
from open_webui.utils.json_codec import JSONCodec
from open_webui.utils.user_visibility_payload import sanitize_user_payload
from starlette.datastructures import MutableHeaders, QueryParams


class UserVisibilityMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)

        start = None
        chunks = []

        async def private_send(message):
            nonlocal start
            if message['type'] == 'http.response.start':
                headers = MutableHeaders(scope=message)
                user = scope.get('state', {}).get('user')
                shared = scope.get('path', '').startswith('/api/v1/chats/share/')
                if (user is not None and user.role != 'admin' or shared and user is None) and (
                    headers.get('content-type', '').split(';')[0] == 'application/json'
                    and 200 <= message['status'] < 300
                    and message['status'] not in {204, 206}
                    and scope.get('method') != 'HEAD'
                    and 'content-disposition' not in headers
                ):
                    start = message
                    return
            if message['type'] == 'http.response.body' and start is not None:
                chunks.append(message.get('body', b''))
                if message.get('more_body', False):
                    return
                data = JSONCodec.loads(b''.join(chunks))
                data = await self._sanitize(scope, data)
                body = JSONCodec.dumps(data).encode('utf-8')
                headers = MutableHeaders(scope=start)
                headers['content-length'] = str(len(body))
                headers['cache-control'] = 'private, no-store'
                for header in ('etag', 'content-md5'):
                    if header in headers:
                        del headers[header]
                await send(start)
                await send({'type': 'http.response.body', 'body': body})
                return
            await send(message)

        await self.app(scope, receive, private_send)

    async def _sanitize(self, scope, data):
        from open_webui.models.channels import Channels
        from open_webui.utils.user_visibility import UserVisibility

        user = scope.get('state', {}).get('user')
        visibility = await UserVisibility.load(user) if user is not None else UserVisibility('', set(), set())
        path = scope.get('path', '')
        channel_id = None
        if path.startswith('/api/v1/channels/'):
            tail = path.removeprefix('/api/v1/channels/').split('/')[0]
            if tail and tail not in {'list', 'create', 'users', 'webhooks'}:
                channel_id = tail
            # Channel lists/creation use the stored channel, never caller data, to
            # decide whether the private-channel identity exception applies.
            if not channel_id:
                items = data if isinstance(data, list) else [data]
                result = []
                for item in items:
                    item_scope = visibility
                    if isinstance(item, dict) and item.get('id'):
                        item_scope = await self._channel_scope(visibility, item['id'], Channels)
                    result.append(sanitize_user_payload(item, item_scope))
                return result if isinstance(data, list) else result[0]
        elif path.startswith('/api/v1/users/'):
            channel_id = QueryParams(scope.get('query_string', b'')).get('channel_id')
        if channel_id and user is not None:
            visibility = await self._channel_scope(visibility, channel_id, Channels)
        return sanitize_user_payload(data, visibility)

    @staticmethod
    async def _channel_scope(visibility, channel_id, channels):
        channel = await channels.get_channel_by_id(channel_id)
        if channel is not None:
            try:
                return await visibility.for_channel(channel)
            except HTTPException:
                # Access can be revoked between the route and serialization.
                pass
        return visibility
