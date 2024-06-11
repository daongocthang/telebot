import uvicorn
import api
import logging
from telegram.ext import Application

from ptb import config, handler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

ptb = Application.builder().token(config).build()
handler.register(ptb)

app = api.creat_app(ptb)

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="127.0.0.1", port=8080, use_colors=False)
    except KeyboardInterrupt:
        logging.info("exit")
