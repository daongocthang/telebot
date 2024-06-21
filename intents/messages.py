import json
import re
from typing import Tuple

from telegram import Update
from ptb.interfaces import Intent
from telegram.ext import ContextTypes, MessageHandler, filters
from ptb import config

with open("knowledge.json", "r", encoding="utf8") as f:
    knowledge = json.load(f)


class DefaultMessage(Intent[MessageHandler]):
    def name(self) -> str:
        return "default_message"

    def _evaluate(self, text: str, pattern: list[str]) -> int:
        words = re.split(r"\s+|[,;?!.-]\s*", text.lower())
        score = 0
        for w in words:
            if w in pattern:
                score += 1
        return score

    def best_response(self, text: str) -> Tuple[int, int]:
        collector = []

        for word in knowledge:
            required_score = 0
            response_score = 0
            required_words = word["keywords"]
            if required_words:
                required_score = self._evaluate(text, required_words)
            if required_score == len(required_words):
                response_score = self._evaluate(text, word["examples"])
            collector.append(response_score)
            # Debugging: Find the best phrase
            # print(response_score, word["examples"])
        highest_score = max(collector)
        return highest_score, collector.index(highest_score)

    def get_response(self, text: str) -> str | None:
        score, index = self.best_response(text)
        if score > 0:
            return knowledge[index]["response"]

    async def reply(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        text = update.message.text
        chat_type = update.message.chat.type
        if chat_type == "group":
            if config.BOT_NAME in text:
                new_text = text.replace(config.BOT_NAME, "").strip()
                response = self.get_response(new_text)
            else:
                return

        else:
            response = self.get_response(text)

        if response:
            await update.message.reply_text(response)

    def handler(self) -> MessageHandler:
        return MessageHandler(filters.TEXT & ~filters.COMMAND, self.reply)
