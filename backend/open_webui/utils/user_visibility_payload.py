"""Viewer-specific account fields; resource ACLs and user-authored metadata stay intact."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from open_webui.utils.user_visibility import UserVisibility

_MENTION = re.compile(r'<@U:([^|>]+)(?:\|[^>]*)?>')
_AVATAR = re.compile(r'/api/v1/users/([^/?]+)/profile/image')
_USER_OBJECTS = {'user', 'owner', 'actor', 'author', 'creator', 'inviter'}
_USER_IDS = {
    'user_id',
    'owner_id',
    'owner_user_id',
    'actor_id',
    'author_id',
    'sender_id',
    'created_by',
    'updated_by',
    'deleted_by',
    'archived_by',
    'pinned_by',
    'invited_by',
}
_USER_LISTS = {'users', 'members', 'participants'}
# A tool may legitimately have a custom parameter named user_id or groups.
_OPAQUE_FIELDS = {'params', 'valves', 'user_valves', 'settings', 'permissions', 'schema', 'spec'}


def sanitize_user_payload(data, visibility: UserVisibility):
    """Never mutate a broadcast/DB payload shared by multiple recipients."""
    if visibility.user_ids is None:
        return data
    return _walk(data, visibility)


def _user_object(value, visibility):
    if not isinstance(value, dict):
        return _walk(value, visibility)
    # Models/webhooks are resource identities, not user accounts.
    if value.get('role') in {'model', 'webhook', 'assistant'}:
        return value.copy()
    if 'id' not in value and 'user_id' not in value:
        return _walk(value, visibility)
    uid = value.get('user_id', value.get('id'))
    return _walk(value, visibility) if visibility.can_see(uid) else None


def _visible_grant(grant, visibility):
    if not isinstance(grant, dict):
        return True
    kind, principal = grant.get('principal_type'), grant.get('principal_id')
    if kind == 'anyone':
        return principal == '*'
    if kind == 'user':
        return principal == '*' or visibility.can_see(principal)
    return kind == 'group' and principal in visibility.group_ids


def _sharing_field(key, value, visibility):
    if key == 'groups' and isinstance(value, list):
        return [
            _walk(group, visibility)
            for group in value
            if not isinstance(group, dict) or 'id' not in group or group['id'] in visibility.group_ids
        ]
    if key == 'group_ids' and isinstance(value, list):
        return [gid for gid in value if gid in visibility.group_ids]
    if key == 'access_grants' and isinstance(value, list):
        return [_walk(grant, visibility) for grant in value if _visible_grant(grant, visibility)]
    return _walk(value, visibility)


def _field(key, value, visibility, *, resource, hidden_owner):
    if resource and key in {'data', 'meta'}:
        # Calendar/note/file metadata is arbitrary client JSON. Message file
        # attachments are embedded resource records and retain identity checks.
        if key == 'data' and isinstance(value, dict) and isinstance(value.get('files'), list):
            return {**value, 'files': _walk(value['files'], visibility)}
        return value
    if key in _OPAQUE_FIELDS:
        return value
    if key in _USER_OBJECTS:
        return _user_object(value, visibility)
    if key in _USER_IDS and isinstance(value, str):
        return value if visibility.can_see(value) else ''
    if key == 'user_ids' and isinstance(value, list):
        return [uid for uid in value if visibility.can_see(uid)]
    if key in _USER_LISTS and isinstance(value, list):
        return [
            clean
            for user in value
            if not isinstance(user, str) or visibility.can_see(user)
            if (clean := _user_object(user, visibility)) is not None
        ]
    if key in {'owner_name', 'user_name', 'author_name'} and hidden_owner:
        return None
    return _sharing_field(key, value, visibility)


def _walk(value, visibility):
    if isinstance(value, str):
        value = _MENTION.sub(lambda m: m[0] if visibility.can_see(m[1]) else '@Unknown', value)
        return _AVATAR.sub(lambda m: m[0] if visibility.can_see(m[1]) else '/user.png', value)
    if isinstance(value, list):
        return [_walk(item, visibility) for item in value]
    if not isinstance(value, dict):
        return value
    if 'id' in value and 'name' in value and value.get('role') in {'admin', 'user', 'pending'}:
        if not visibility.can_see(value['id']):
            return None
    hidden_owner = any(
        value.get(key) and not visibility.can_see(value[key])
        for key in ('user_id', 'owner_id', 'owner_user_id', 'author_id')
    )
    result = {
        key: _field(key, item, visibility, resource='id' in value and 'user_id' in value, hidden_owner=hidden_owner)
        for key, item in value.items()
    }
    # OpenAPI/MCP tool DTOs reuse user_id for their server identifier.
    resource_id = value.get('id')
    if isinstance(resource_id, str) and resource_id.startswith('server:') and value.get('user_id') == resource_id:
        result['user_id'] = resource_id
    if isinstance(result.get('users'), list) and 'count' in result:
        result['count'] = len(result['users'])
    return result
