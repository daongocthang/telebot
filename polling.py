import logging
from telegram import Update
from telegram.ext import Application

from ptb import config, member, utils
from ptb.executor import IntentExecutor

utils.set_logging_httpx()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        ptb = Application.builder().token(config.BOT_TOKEN).build()
        ptb.add_handler(member.handler)
        executor = IntentExecutor()
        executor.register("intents", ptb)

        ptb.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        pass
