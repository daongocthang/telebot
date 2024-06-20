from typing import Final
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CommandHandler,
)
from telegram.constants import ParseMode
from ptb.interfaces import Intent
from ptb.config import dbase
from ptb.types import ChatInfo, admin_only
from ptb.utils import from_dict
from ptb.const import emoji

message_input: Final[str] = "Vui lòng nhập mã bảo hành."
message_choice: Final[str] = "Những trường hợp này như thế nào?!"
message_report_sent: Final[str] = "{0} đã gửi đến {1}."
message_not_found: Final[str] = "{0} không tìm thấy."
message_send_failure: Final[str] = (
    "{0} chưa có trên Hệ thống BH "
    + emoji.DISAPPOINT_FACE
    + "\n{1} bảo CH tiếp nhận trước."
)
message_send_success: Final[str] = (
    " {0} đã trả CM " + emoji.PARTY_POPPER + "\n{1} lh CH để xác nhận."
)

stage0, stage1 = range(2)


class ResultConvos(Intent[ConversationHandler]):
    __slots__ = "result_ok"

    def __init__(self) -> None:
        self.result_ok: bool

    def name(self) -> str:
        return "success_convos"

    @admin_only
    async def _choose_result(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        choice = [
            ["success"],
            ["failure"],
        ]
        reply_markup = ReplyKeyboardMarkup(choice, one_time_keyboard=True)
        await update.message.reply_text(message_choice, reply_markup=reply_markup)
        return stage0

    async def _input_tickets(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        text = update.message.text.lower()

        self.result_ok = "success" in text
        await update.message.reply_text(
            message_input, reply_markup=ReplyKeyboardRemove()
        )
        return stage1

    async def _post_result(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        tickets = update.message.text.split("\n")
        data = dbase.get()
        reply_text = message_send_success if self.result_ok else message_send_failure
        for key in tickets:
            if key in data.keys():
                chat_info = from_dict(ChatInfo, data.get(key))
                dbase.drop(key)
                await context.bot.send_message(
                    chat_id=chat_info.chat_id,
                    reply_to_message_id=chat_info.message_id,
                    text=reply_text.format(key, chat_info.mention),
                    parse_mode=ParseMode.HTML,
                )
                await update.message.reply_html(
                    message_report_sent.format(key, chat_info.mention)
                )
            else:
                await update.message.reply_html(message_not_found.format(key))

        return ConversationHandler.END

    def handler(self) -> ConversationHandler:
        return ConversationHandler(
            entry_points=[CommandHandler("send", self._choose_result)],
            states={
                stage0: [
                    MessageHandler(
                        filters.Regex("^(success|failure)"), self._input_tickets
                    )
                ],
                stage1: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self._post_result)
                ],
            },
            fallbacks=[MessageHandler(filters.Regex("(done|cancel)$"), self.end_convo)],
        )
