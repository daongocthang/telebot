import json
from dotenv import load_dotenv
from os import getenv

load_dotenv()


BOT_TOKEN = getenv("BOT_TOKEN")
WEBHOOK_URL = getenv("WEBHOOK_URL")

FIREBASE_CREDENTIALS = json.loads(getenv("FIREBASE_CREDENTIALS"))
FIREBASE_URL = getenv("FIREBASE_URL")
