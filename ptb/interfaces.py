from typing import Generic, TypeVar
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

T = TypeVar("T")


class Action:
    async def callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int | None:
        raise NotImplementedError("An action must implement its callback method")


class Intent(Generic[T]):
    def name(self) -> str:
        raise NotImplementedError("An intent must implement a name")

    def handler(self) -> T:
        raise NotImplementedError("An intent must implement its handler method")

    async def end_convo(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
        return ConversationHandler.END

    def __str__(self) -> str:
        return " ".join([self.__class__.__name__, self.name()])
