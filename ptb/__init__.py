import functools
import logging

from telegram import Update
from ptb import config


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
            logging.error(e)

    return wrapper
