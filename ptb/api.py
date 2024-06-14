from contextlib import asynccontextmanager
from http import HTTPStatus
from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse
from telegram import Update
from telegram.ext import Application
from ptb import config
from ptb import handler
from typing import AsyncGenerator

from ptb.db.firebase import FirebasePersistence


# build a Python Telegram Bot
fb_persistence = FirebasePersistence.from_env()
ptb = Application.builder().persistence(fb_persistence).token(config.BOT_TOKEN).build()
handler.register(ptb)


# create a fastapi app
def creat_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncGenerator:
        await ptb.bot.set_webhook(
            url=f"{config.WEBHOOK_URL}/webhook", allowed_updates=Update.ALL_TYPES
        )
        async with ptb:
            await ptb.start()
            yield
            await ptb.stop()

    app = FastAPI(lifespan=lifespan)

    @app.get("/healthcheck")
    async def health() -> PlainTextResponse:
        return PlainTextResponse(
            content="The bot is still running fine :)", status_code=HTTPStatus.OK
        )

    @app.post("/webhook")
    async def process_update(request: Request) -> Response:
        req = await request.json()
        update = Update.de_json(data=req, bot=ptb.bot)
        await ptb.process_update(update)
        return Response(status_code=HTTPStatus.OK)

    return app
