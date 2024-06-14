from telegram.ext import Application

from . import chat_member, command


def register(application: Application) -> None:
    application.add_handlers(chat_member.handlers)
    for handler in command.handlers:
        application.add_handler(handler)
