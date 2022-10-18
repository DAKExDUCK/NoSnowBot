import logging
from functools import wraps

from aiogram import types

logger = logging.getLogger('aiogram.dispatcher.dispatcher')


def log_msg(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        message: types.Message = args[0]
        if message.chat.id == message.from_user.id:
            logger.info(f"{message.from_user.id} - {message.text}")
        else:
            logger.info(
                f"{message.from_user.id} / {message.chat.id} - {message.text}")
        return func(*args, **kwargs)
    return wrapper
