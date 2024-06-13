from http import HTTPStatus
from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import Application, CommandHandler
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn


from ptb import config
from ptb.handler import command

if __name__ == "__main__":
    ptb = Application.builder().token(config.BOT_TOKEN).build()

    ptb.add_handler(CommandHandler("start", command.start))

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncGenerator:
        await ptb.bot.set_webhook(
            f"{config.WEBHOOK_URL}/webhook", allowed_updates=Update.ALL_TYPES
        )
        async with ptb:
            await ptb.start()
            yield
            await ptb.stop()

    app = FastAPI(lifespan=lifespan)

    @app.post("/webhook")
    async def process_update(req: Request) -> Response:
        json_dict = await req.json()
        update = Update.de_json(data=json_dict, bot=ptb.bot)
        await ptb.process_update(update)
        return Response(HTTPStatus.OK)

    if __name__ == "__main__":
        uvicorn.run(app=app, host="127.0.0.1", port=8080, use_colors=False)
