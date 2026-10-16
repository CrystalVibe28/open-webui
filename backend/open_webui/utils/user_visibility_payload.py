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
_USER_LISTS = {'users', 'members', 'participants', 'attendees'}
# A tool may legitimately have a custom parameter named user_id or groups.
_OPAQUE_FIELDS = {'params', 'valves', 'user_valves', 'settings', 'permissions', 'schema', 'spec', 'specs'}
# Records the server embeds in a resource's otherwise arbitrary data/meta JSON:
# message attachments, arena grants and legacy model knowledge.
_EMBEDDED = {'data': ('files',), 'meta': ('access_grants', 'knowledge')}


def sanitize_user_payload(data, visibility: UserVisibility):
    """Never mutate a broadcast/DB payload shared by multiple recipients."""
    if visibility.user_ids is None:
        return data
    return _walk(data, visibility)


def _user_object(value, visibility, hidden_owner=False):
    if not isinstance(value, dict):
        return _walk(value, visibility)
    # Models/webhooks/apps are resource identities, not user accounts.
    if value.get('role') in {'model', 'webhook', 'assistant', 'app'}:
        return value.copy()
    if 'id' not in value and 'user_id' not in value:
        # Version history entries carry only the author's name next to their own user_id.
        return None if hidden_owner else _walk(value, visibility)
    uid = value.get('user_id', value.get('id'))
    return _walk(value, visibility) if visibility.can_see(uid) else None


def _is_grant(value):
    return isinstance(value, dict) and 'principal_type' in value and 'principal_id' in value


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
    if key == 'parent_group_id' and isinstance(value, str):
        return value if value in visibility.group_ids else None
    return _walk(value, visibility)


def _field(key, value, visibility, *, resource, hidden_owner):
    if resource and key in {'data', 'meta'}:
        # Calendar/note/file metadata is arbitrary client JSON; only the embedded
        # resource records retain identity checks.
        if isinstance(value, dict):
            embedded = {
                name: _sharing_field(name, value[name], visibility)
                for name in _EMBEDDED[key]
                if isinstance(value.get(name), list)
            }
            if embedded:
                return {**value, **embedded}
        return value
    if key in _OPAQUE_FIELDS:
        return value
    if key in _USER_OBJECTS:
        return _user_object(value, visibility, hidden_owner)
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
        # A bare list of grants has no access_grants key to mark it.
        return [_walk(item, visibility) for item in value if not _is_grant(item) or _visible_grant(item, visibility)]
    if not isinstance(value, dict):
        return value
    # Values are type-checked because a JSON schema reuses these names for nested dicts.
    role = value.get('role')
    if 'id' in value and 'name' in value and isinstance(role, str) and role in {'admin', 'user', 'pending'}:
        if not visibility.can_see(value['id']):
            return None
    hidden_owner = any(
        isinstance(value.get(key), str) and value[key] and not visibility.can_see(value[key])
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
