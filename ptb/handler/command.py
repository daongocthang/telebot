from dataclasses import asdict, dataclass
import logging
import re
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from ptb.db import dbutils
from ptb.db.firebase import FirebaseDatabase
from ptb.utils import emoji

from ptb import admin_only


@dataclass
class DataInput:
    chat_id: int | str
    message_id: int
    mention: str
    todict = asdict


db = FirebaseDatabase.from_env()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Python Telegram Bot")


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_data = dbutils.ChatData(context)
        pattern = re.compile(r"^TNBH[0-9]{7}$")
        ticket = context.args[0]
        logging.info(ticket)
        ticket = ticket.strip()
        if pattern.match(ticket):
            # push to db
            db.update(
                ticket,
                DataInput(
                    chat_id=update.message.chat_id,
                    message_id=update.message.id,
                    mention=update.effective_user.mention_html(),
                ).todict(),
            )
            await update.message.reply_html(f"{emoji.OK_HAND} Bạn chờ BHKV xử lý nhé!")
        else:
            await update.message.reply_html(f"Mã bảo hành không đúng {emoji.NO_ENTRY}")
    except IndexError:
        await update.message.reply_html(f"Không có mã bảo hành {emoji.DISAPPOINT_FACE}")


@admin_only
async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(db.get())


@admin_only
async def rem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ticket = context.args[0]
    pass


handlers = [
    CommandHandler(["start", "help"], start),
    CommandHandler("add", add),
    CommandHandler("show", show),
]
