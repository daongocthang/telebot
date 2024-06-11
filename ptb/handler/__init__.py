from telegram.ext import Application, CommandHandler
from . import callback


def register(application: Application) -> None:
    application.add_handler(CommandHandler("start", callback.start))
