from typing import Optional

from telegram import ChatMember, ChatMemberUpdated


def is_admin(status: str) -> bool:
    return status in [
        ChatMember.ADMINISTRATOR,
        ChatMember.OWNER,
    ]


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
