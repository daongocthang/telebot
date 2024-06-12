from telegram.ext import Application
from . import command


def register(application: Application) -> None:
    application.add_handlers(handlers=command.handlers)
