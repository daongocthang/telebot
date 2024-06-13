import random
from telegram import Update
from telegram.ext import ContextTypes, ChatMemberHandler
from telegram.constants import ParseMode

from ptb.utils import emoji, member


async def greeting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = member.status_change(update.chat_member)
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

        text = f"Chào mừng {member_name} đã tham gia nhóm."
        if member_name != cause_name:
            text += f"\nCảm ơn {cause_name} đã mời {member_name}."

        await update.effective_chat.send_message(text, parse_mode=ParseMode.HTML)


handlers = [ChatMemberHandler(greeting, ChatMemberHandler.CHAT_MEMBER)]
