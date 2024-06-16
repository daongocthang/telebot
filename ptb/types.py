from dataclasses import dataclass
import functools
import logging

from telegram import Update

from ptb import config

logger = logging.getLogger(__name__)


@dataclass
class ChatInfo:
    chat_id: int | str
    message_id: int
    mention: str

    def todict(self):
        return self.__dict__.copy()


def admin_only(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            for a in args:
                if isinstance(a, Update):
                    update = a  # type: Update
                    break
            if not update:
                raise TypeError("Argument update is not found.")

            if str(update.message.chat_id) == config.ADMIN_CHAT_ID:
                return await func(*args, **kwargs)
            else:
                raise PermissionError("Allow for group admin only.")
        except (TypeError, PermissionError) as e:
            logger.warning(e)

    return wrapper
