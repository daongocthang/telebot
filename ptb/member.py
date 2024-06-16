import random
from typing import Final, Optional
from telegram import Update, ChatMember, ChatMemberUpdated
from telegram.ext import ContextTypes, ChatMemberHandler
from telegram.constants import ParseMode
from ptb.const import emoji

message_greeting: Final[str] = "Chào mừng {0} đã tham gia nhóm. /help"
message_thanks: Final[str] = "\nCảm ơn {0} đã mời {0}."


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


async def greeting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = status_change(update.chat_member)
    if result is None:
        return

    was_member, is_member = result
    cause_name = update.chat_member.from_user.mention_html()
    member_name = update.chat_member.new_chat_member.user.mention_html()

    has_joined = not was_member and is_member
    # has_left = was_member and not is_member

    if has_joined:
        emoji_list = [emoji.PARTY_POPPER, emoji.PARTYING_FACE, emoji.CONFETTI_BALL]

        await update.effective_chat.send_message(random.choice(emoji_list))

        text = message_greeting.format(member_name)
        if member_name != cause_name:
            text += message_thanks.format(cause_name, member_name)

        await update.effective_chat.send_message(text, parse_mode=ParseMode.HTML)


handler = ChatMemberHandler(greeting, ChatMemberHandler.CHAT_MEMBER)
