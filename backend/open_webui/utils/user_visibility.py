from dataclasses import dataclass

from fastapi import HTTPException, status


def is_open_channel(channel) -> bool:
    """Open channels are read across groups, so their viewers do not share one visible set."""
    from open_webui.models.access_grants import has_public_read_access_grant

    if channel.type == 'dm':
        return False
    if channel.type == 'group' and channel.is_private is not None:
        return channel.is_private is False
    return has_public_read_access_grant(channel.access_grants)


async def get_admin_ids(db=None) -> set[str]:
    """Admins run the instance and own its shared models and tools, so every user sees them."""
    from open_webui.internal.db import get_async_db_context
    from open_webui.models.users import User
    from sqlalchemy import select

    async with get_async_db_context(db) as session:
        return set((await session.execute(select(User.id).where(User.role == 'admin'))).scalars().all())


@dataclass
class UserVisibility:
    user_id: str
    user_ids: set[str] | None
    group_ids: set[str] | None

    @classmethod
    async def common(cls, user_id, db=None):
        """The users every viewer sees, for content that is read across groups."""
        return cls(user_id, await get_admin_ids(db), set())

    @classmethod
    async def load(cls, user, db=None):
        if user.role == 'admin':
            return cls(user.id, None, None)

        from open_webui.models.groups import Groups

        groups = await Groups.get_groups_by_member_id(user.id, db=db)
        group_ids = {group.id for group in groups}
        user_ids = {user.id} | await get_admin_ids(db)
        if group_ids:
            memberships = await Groups.get_group_user_ids_by_ids(list(group_ids), db=db)
            user_ids.update(user_id for member_ids in memberships.values() for user_id in member_ids)
        return cls(user.id, user_ids, group_ids)

    @classmethod
    async def load_for_request(cls, user, channel_id=None, db=None):
        visibility = await cls.load(user, db=db)
        if channel_id is None or visibility.user_ids is None:
            return visibility

        from open_webui.models.channels import Channels

        channel = await Channels.get_channel_by_id(channel_id, db=db)
        if channel is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return await visibility.for_channel(channel, db=db)

    async def for_channel(self, channel, db=None):
        if self.user_ids is None:
            return self

        from open_webui.models.access_grants import AccessGrants
        from open_webui.models.channels import Channels
        from open_webui.models.config import Config
        from open_webui.utils.access_control import has_permission

        if not await Config.get('channels.enable') or not await has_permission(
            self.user_id, 'features.channels', await Config.get('user.permissions')
        ):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        if channel.type in {'group', 'dm'}:
            if not await Channels.is_user_channel_member(channel.id, self.user_id, db=db):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            if is_open_channel(channel):
                return self
            members = await Channels.get_members_by_channel_id(channel.id, db=db)
            user_ids = {member.user_id for member in members if member.is_active}
            return UserVisibility(self.user_id, user_ids, self.group_ids)

        if not await AccessGrants.has_access(
            user_id=self.user_id,
            resource_type='channel',
            resource_id=channel.id,
            permission='read',
            user_group_ids=self.group_ids,
            db=db,
        ):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if is_open_channel(channel):
            return self

        users = await AccessGrants.get_users_with_access(
            resource_type='channel', resource_id=channel.id, permission='read', db=db
        )
        # Admins can read every standard channel without a grant.
        return UserVisibility(
            self.user_id,
            {user.id for user in users if user.role != 'pending'} | {channel.user_id} | await get_admin_ids(db),
            self.group_ids,
        )

    def can_see(self, user_id: str) -> bool:
        return self.user_ids is None or isinstance(user_id, str) and user_id in self.user_ids

    def require_user(self, user_id: str) -> None:
        if not self.can_see(user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    def require_group(self, group_id: str) -> None:
        if self.group_ids is not None and group_id not in self.group_ids:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    def filter_users(self, users: list):
        if self.user_ids is None:
            return users
        return [user for user in users if user.id in self.user_ids]
