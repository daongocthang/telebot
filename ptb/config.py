import json
import logging
from dotenv import load_dotenv
from os import getenv


load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
WEBHOOK_URL = getenv("WEBHOOK_URL")

FIREBASE_CREDENTIALS = json.loads(getenv("FIREBASE_CREDENTIALS"))
# f = open("firebase.json", "rb")
# FIREBASE_CREDENTIALS = json.load(f)

FIREBASE_URL = getenv("FIREBASE_URL")
ADMIN_CHAT_ID = getenv("ADMIN_CHAT_ID")


def get_logger(name: str | None = None) -> logging.Logger:
    # Enable logging
    logging.basicConfig(
        format="[%(asctime)s %(levelname)s] %(name)s - %(message)s", level=logging.INFO
    )
    # set higher logging level for httpx to avoid all GET and POST requests being logged
    logging.getLogger("httpx").setLevel(logging.WARNING)

    return logging.getLogger(__name__)
