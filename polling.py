from telegram import Update
from telegram.ext import Application, CommandHandler

from ptb import config
from ptb.handler import command

logger = config.get_logger(__name__)

if __name__ == "__main__":
    try:
        ptb = Application.builder().token(config.BOT_TOKEN).build()
        ptb.add_handler(CommandHandler("start", command.start))
        ptb.add_handler(CommandHandler("add", command.add))
        ptb.add_handler(CommandHandler("show", command.show))

        ptb.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        pass
