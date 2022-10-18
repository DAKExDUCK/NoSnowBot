import asyncio
import logging.config

from aiohttp import web

from config import bot, log_config
from modules.bot.main import start_bot

routes = web.RouteTableDef()
logging.config.dictConfig(log_config)


async def make_app():
    asyncio.create_task(start_bot(bot))
    app = web.Application()

    return app

web.run_app(make_app())