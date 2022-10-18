import asyncio
import aiomysql
import aioredis

loop = asyncio.get_event_loop()


class DB:
    conn: aiomysql.Connection

    async def start_db(SQL_HOST, SQL_PORT, SQL_USER, SQL_PASSWD, SQL_DB):
        DB.conn = await aiomysql.connect(host=SQL_HOST, port=int(SQL_PORT),
                                        user=SQL_USER, password=SQL_PASSWD, db=SQL_DB,
                                        loop=loop)


class Redis:
    redis: aioredis.Redis

    async def start_redis(user, passwd, host, port, db):
        Redis.redis = await aioredis.from_url(f"redis://{host}:{port}/{db}", password=passwd, decode_responses=True)
