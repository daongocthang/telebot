from dotenv import load_dotenv
from os import getenv

load_dotenv()

has_env = getenv("ENV") is not None

BOT_TOKEN = getenv("BOT_TOKEN")
BOT_HOST = getenv("BOT_HOST")
WEBHOOK_URL = getenv("WEBHOOK_URL")
