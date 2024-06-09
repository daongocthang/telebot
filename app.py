from http import HTTPStatus as status
from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler
import uvicorn
from ptb import config
from contextlib import asynccontextmanager
import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Starting...")


ptb = Application.builder().updater(None).token(config.BOT_TOKEN).build()
ptb.add_handler(CommandHandler("start", start))


@asynccontextmanager
async def lifespan(_: FastAPI):
    await ptb.bot.set_webhook(config.WEBHOOK_URL)
    async with ptb:
        await ptb.start()
        yield
        await ptb.stop()


app = FastAPI(lifespan=lifespan)


@app.get("/healthcheck")
async def health() -> PlainTextResponse:
    return PlainTextResponse(
        content="The bot is still running fine :)", status_code=status.OK
    )


@app.post("/webhook")
async def process_update(request: Request) -> Response:
    req = await request.json()
    update = Update.de_json(data=req, bot=ptb.bot)
    await ptb.process_update(update)
    return Response(status_code=status.OK)


if __name__ == "__main__":
    try:
        uvicorn.run(app, host="127.0.0.1", port=8080, use_colors=False)
    except KeyboardInterrupt:
        logging.info("exit")
