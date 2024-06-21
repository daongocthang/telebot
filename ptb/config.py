import json
from typing import Final
from dotenv import load_dotenv, find_dotenv
from os import getenv

from ptb.db.firebase import FirebaseDatabase


load_dotenv(find_dotenv())

BOT_TOKEN: Final[str] = getenv("BOT_TOKEN")
BOT_NAME: Final[str] = getenv("BOT_NAME")
WEBHOOK_URL: Final[str] = getenv("WEBHOOK_URL")

FIREBASE_CREDENTIALS: Final[str] = json.loads(getenv("FIREBASE_CREDENTIALS"))

FIREBASE_URL: Final[str] = getenv("FIREBASE_URL")
ADMIN_CHAT_ID: Final[str] = getenv("ADMIN_CHAT_ID")

dbase = FirebaseDatabase.from_env()
