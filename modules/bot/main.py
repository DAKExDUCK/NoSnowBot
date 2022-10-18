from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.types import BotCommand
from config import (REDIS_DB, REDIS_HOST, REDIS_PASSWD, REDIS_PORT, REDIS_USER,
                    SQL_DB, SQL_HOST, SQL_PASSWD, SQL_PORT, SQL_USER)

from ..database.main import DB, Redis
from .handlers.admin import register_handlers_admin
from .handlers.default import register_handlers_default
from .handlers.kamaz import register_handlers_for_kamaz


async def set_commands(bot):
    commands = [
        BotCommand(command="/start", description="Start | Info"),
        BotCommand(command="/help", description="Help | Commands"),
    ]
    await bot.set_my_commands(commands)


async def start_bot(bot):
    await DB.start_db(SQL_HOST, SQL_PORT, SQL_USER, SQL_PASSWD, SQL_DB)
    await Redis.start_redis(REDIS_USER, REDIS_PASSWD, REDIS_HOST, REDIS_PORT, REDIS_DB)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_admin(dp)
    register_handlers_default(dp)

    register_handlers_for_kamaz(dp)
    
    await set_commands(bot)

    await dp.start_polling()
