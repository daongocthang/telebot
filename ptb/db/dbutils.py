from typing import NamedTuple
from telegram.ext import BasePersistence


class UserData:
    def __init__(self, persistence: BasePersistence) -> None:
        self.persistence = persistence

    async def get(self, user_id: int) -> dict:
        return await self.persistence.get_user_data(user_id)

    async def update(self, user_id: int, data: dict) -> None:
        await self.persistence.update_user_data(user_id, data)

    async def drop(self, user_id: int) -> None:
        await self.persistence.drop_user_data(user_id)
