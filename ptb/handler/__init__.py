from telegram.ext import Application
from . import command, chat_member

MESSAGE = -1
COMMAND, CHAT_MEMBER = range(2)


def register(application: Application) -> None:
    application.add_handlers(
        handlers={COMMAND: command.handlers, CHAT_MEMBER: chat_member.handlers}
    )
