import logging
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Python Telegram Bot")


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    context.bot.delete_messages(chat_id)

    await update.message.reply_text("testing clear chat history")


handlers = [CommandHandler(["start", "help"], start), CommandHandler("clear", clear)]
