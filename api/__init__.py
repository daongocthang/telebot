from contextlib import asynccontextmanager
from http import HTTPStatus
from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse
from telegram import Update
from telegram.ext import Application
from ptb import config
from ptb import handler


def creat_app(ptb: Application) -> FastAPI:
    @asynccontextmanager
    async def lifespan(_: FastAPI):
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
