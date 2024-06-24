import logging
import random
import re
from typing import Dict, Final
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from ptb.const import emoji
from ptb.interfaces import Intent
from ptb.types import ChatInfo, admin_only
from ptb.config import dbase

message_empty_data: Final[str] = "Không có dữ liệu."
message_success: Final[str] = (
    random.choice([emoji.THUMB_UP, emoji.OK_HAND]) + " {0} chờ BHKV xử lý nhé!"
)
message_failure: Final[str] = f"Mã bảo hành không đúng {emoji.NO_ENTRY}"
message_error: Final[str] = f"Không có mã bảo hành {emoji.DISAPPOINT_FACE}"
message_help: Final[Dict[str, str]] = {
    "private": '{0} vui lòng tham gia nhóm <a href="https://t.me/+AlE4kevmxlM5OWRl">Hỗ trợ Bảo hành</a>',
    "group": "Bạn có thể gửi cú pháp sau:\n\n/traht <code>MA_BAO_HANH</code> - trả hệ thống không chuyển vật lý",
}
message_deprecated: Final[str] = (
    "Cú pháp này không còn dùng nữa. Bạn gửi /help để xem hướng dẫn."
)

logger = logging.getLogger(__name__)


class HelpCommandHandler(Intent[CommandHandler]):
    def name(self) -> str:
        return "start_command"

    async def _help_command(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        chat_type = update.message.chat.type
        mention = update.effective_user.mention_html()
        await update.message.reply_html(
            message_help.get(chat_type).format(mention if mention else "")
        )

    def handler(self) -> CommandHandler:
        return CommandHandler(["start", "help"], self._help_command)


class SupportCommandHandler(Intent[CommandHandler]):
    def name(self) -> str:
        return "support_command"

    async def _update_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        try:
            pattern = re.compile(r"^TNBH[0-9]{7}$")
            ticket = context.args[0]
            ticket = ticket.strip()
            user_mention = update.effective_user.mention_html()
            if pattern.match(ticket):
                # push to db
                dbase.update(
                    ticket,
                    ChatInfo(
                        chat_id=update.message.chat_id,
                        message_id=update.message.id,
                        mention=user_mention,
                    ).todict(),
                )
                await update.message.reply_html(message_success.format(user_mention))
            else:
                await update.message.reply_html(message_failure)
        except IndexError:
            await update.message.reply_html(message_error)

    def handler(self) -> CommandHandler:
        return CommandHandler("tra_ht", self._update_command)


class ShowCommandHandler(Intent[CommandHandler]):
    def name(self) -> str:
        return "show_command"

    @admin_only
    async def _get_command(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        data = dbase.get().keys()
        await update.message.reply_text("\n".join(data) if data else message_empty_data)

    def handler(self) -> CommandHandler:
        return CommandHandler("show", self._get_command)


class WhoAmI(Intent[CommandHandler]):
    def name(self) -> str:
        return "who_am_i"

    async def _command(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.message.chat_id
        if update.message.chat.type == "private":
            await update.message.reply_text(f"chat_id: {chat_id}")
        else:
            logger.warning(f"`{self.name()}` is denied in a group")

    def handler(self) -> CommandHandler:
        return CommandHandler("whoami", self._command)


class DeprecatedCommand(Intent[MessageHandler]):
    def name(self) -> str:
        return "deprecated_command"

    async def _callback(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_html(message_deprecated)

    def handler(self) -> MessageHandler:
        return MessageHandler(
            filters.Regex(r"^/?(hotro_tra_ht|tra_ht)"), self._callback
        )
