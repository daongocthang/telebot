from typing import NamedTuple
from telegram.ext import BasePersistence


class UserData:
    def __init__(self, persistence: BasePersistence) -> None:
        self.persistence = persistence

    async def get(self) -> dict:
        return await self.persistence.get_user_data()

    async def update(self, user_id: int, data: dict) -> None:
        await self.persistence.update_user_data(user_id, data)

    async def drop(self, user_id: int) -> None:
        await self.persistence.drop_user_data(user_id)


class ChatData:
    def __init__(self, persistence: BasePersistence) -> None:
        self.persistence = persistence

    async def get(self) -> dict:
        return await self.persistence.get_chat_data

    async def update(self, chat_id: int, data: any) -> None:
        await self.persistence.update_chat_data(chat_id, data)

    async def drop(self, chat_id: int) -> None:
        await self.persistence.drop_chat_data(chat_id)
