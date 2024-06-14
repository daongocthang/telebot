from typing import Any
from telegram.ext import ContextTypes


class UserData:
    def __init__(self, context: ContextTypes.DEFAULT_TYPE) -> None:
        self.persistence = context.application.persistence
        self.__user_data = context.application.user_data

    async def get(self) -> dict:
        return await self.persistence.get_user_data()

    async def update(self, user_id: int, data: Any) -> None:
        if data:
            self.__user_data[user_id] = data
        await self.persistence.update_user_data(user_id, data)

    async def drop(self, user_id: int) -> None:
        if user_id in self.__user_data.keys():
            del self.__user_data[user_id]
        await self.persistence.drop_user_data(user_id)


class ChatData:
    def __init__(self, context: ContextTypes.DEFAULT_TYPE) -> None:
        self.persistence = context.application.persistence
        self.__chat_data = context.application.chat_data

    async def get(self):
        return await self.persistence.get_chat_data()

    async def update(self, chat_id: int, data: Any) -> None:
        if data:
            self.__chat_data[chat_id] = data
        await self.persistence.update_chat_data(chat_id, data)

    async def drop(self, chat_id: int) -> None:
        if chat_id in self.__chat_data.keys():
            del self.__chat_data[chat_id]
        await self.persistence.drop_chat_data(chat_id)
