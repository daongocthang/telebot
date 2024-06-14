from dataclasses import asdict, dataclass
import logging
import re
from typing import Any, Mapping, NamedTuple
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from ptb.db import dbutils
from ptb.utils import emoji

from ptb import admin_only


@dataclass
class DataInput:
    message_id: int
    ticket: str
    todict = asdict

    def map(self, data: dict) -> None:
        data[self.ticket] = self.message_id


class DataResult(NamedTuple):
    chat_id: int | str
    message_id: int
    mention: str


def parse(chat_data: Mapping) -> dict[str, Any]:
    return {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Python Telegram Bot")


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_data = dbutils.ChatData(context)
        pattern = re.compile(r"^TNBH[0-9]{7}$")
        ticket = context.args[0]
        logging.info(ticket)
        ticket = ticket.strip()
        if pattern.match(ticket):
            chat_data.update(
                update.message.chat_id,
                {update.message.id, ticket},
            )
            await update.message.reply_html(f"{emoji.OK_HAND} Bạn chờ BHKV xử lý nhé!")
        else:
            await update.message.reply_html(f"Mã bảo hành không đúng {emoji.NO_ENTRY}")
    except IndexError:
        await update.message.reply_html(f"Không có mã bảo hành {emoji.DISAPPOINT_FACE}")


@admin_only
async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_data = dbutils.ChatData(context)
    resp = await chat_data.get()
    await update.message.reply_text(resp)


@admin_only
async def rem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ticket = context.args[0]
    pass


handlers = [
    CommandHandler(["start", "help"], start),
    CommandHandler("add", support),
    CommandHandler("show", show),
]
