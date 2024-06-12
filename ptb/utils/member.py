import functools
import logging
from typing import Optional

from telegram import ChatMember, ChatMemberUpdated, Update


def is_admin(status: str) -> bool:
    return status in [
        ChatMember.ADMINISTRATOR,
        ChatMember.OWNER,
    ]


def admin_only(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            for a in args:
                if isinstance(a, Update):
                    update = a  # type: Update
                    break
            if not update:
                raise TypeError("Argument update is not found.")

            user_id = await update.message.from_user.id
            member = update.effective_chat.get_member(user_id)  # type: ChatMember
            if member.status and is_admin(member.status):
                return await func(*args, **kwargs)
            else:
                raise PermissionError("Allow for group admin only.")
        except (TypeError, PermissionError) as e:
            logging.error(e)

    return wrapper


def status_change(chat_member_update: ChatMemberUpdated) -> Optional[tuple[bool, bool]]:
    status_change = chat_member_update.difference().get("status")
    is_old_member, is_new_member = chat_member_update.difference().get(
        "is_member", (None, None)
    )

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = old_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (old_status == ChatMember.RESTRICTED and is_old_member is True)
    is_member = new_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (new_status == ChatMember.RESTRICTED and is_new_member is True)

    return was_member, is_member
