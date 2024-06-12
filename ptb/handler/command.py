import logging
import re
from typing import NamedTuple
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from ptb.db import dbutils
from ptb.utils import emoji, member


class DataInput(NamedTuple):
    message_id: int
    mention: str
    data: any


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Python Telegram Bot")


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_data = dbutils.ChatData(context.application.persistence)
        pattern = re.compile(r"^TTBH[0-9]{7}$")
        ticket = context.args[0]
        ticket = ticket.strip()
        if pattern.match(ticket):
            chat_data.update(
                update.message.chat_id,
                DataInput(
                    message_id=update.message.id,
                    mention=update.effective_user.mention_html(),
                    data=ticket,
                ),
            )
            await update.message.reply_text(f"{emoji.OK_HAND} Bạn chờ BHKV xử lý nhé!")
        else:
            await update.message.reply_text(f"Mã bảo hành không đúng {emoji.NO_ENTRY}")
    except (IndexError, ValueError):
        await update.message.reply_text(f"Không có mã bảo hành {emoji.DISAPPOINT_FACE}")


@member.admin_only
async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = dbutils.ChatData(context.application.persistence)
    await update.message.reply_text("")


handlers = [CommandHandler(["start", "help"], start), CommandHandler("clear", clear)]
