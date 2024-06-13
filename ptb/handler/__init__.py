from telegram.ext import Application, CommandHandler
from . import command, chat_member

MESSAGE = -1
COMMAND, CHAT_MEMBER = range(2)


def register(application: Application) -> None:
    application.add_handler(CommandHandler("start", command.handlers))
