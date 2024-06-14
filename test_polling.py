from telegram import Update
from telegram.ext import Application, CommandHandler

from ptb import config
from ptb.db.firebase import FirebasePersistence
from ptb.handler import command

logger = config.get_logger(__name__)

if __name__ == "__main__":
    persistence = FirebasePersistence.from_env()
    ptb = Application.builder().persistence(persistence).token(config.BOT_TOKEN).build()
    ptb.add_handler(CommandHandler("start", command.start))
    ptb.add_handler(CommandHandler("add", command.support))
    ptb.add_handler(CommandHandler("show", command.show))

    ptb.run_polling(allowed_updates=Update.ALL_TYPES)
