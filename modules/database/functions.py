import json
from .main import DB, Redis


# SQL
async def insert_new_request(data):
    async with DB.conn.cursor() as cur:
        query = ("INSERT INTO request VALUES("
            f"{data['user_id']},"
            f"{data['role']},"
            f"'{data['name']}',"
            f"1,"
            f"'{data['phone_number']}',"
            f"'{data['state_number']}'"
            ");")
        await cur.execute(query)
        await DB.conn.commit()


async def get_request(id):
    async with DB.conn.cursor() as cur:
        query = f"SELECT * FROM request WHERE idrequest='{id}'"
        await cur.execute(query)
        result = (await cur.fetchall())[0]
    data = {}
    data['user_id'] = result[0]
    data['role'] = result[1]
    data['name'] = result[2]
    data['status'] = result[3]
    data['phone_number'] = result[4]
    data['state_number'] = result[5]
    return data


async def delete_request(id):
    async with DB.conn.cursor() as cur:
        query = f"DELETE FROM request WHERE idrequest='{id}'"
        await cur.execute(query)
        await DB.conn.commit()


async def insert_new_kamaz(data):
    async with DB.conn.cursor() as cur:
        query = ("INSERT INTO kamaz VALUES("
            f"{data['user_id']},"
            f"'{data['name']}',"
            f"0,"
            f"'{data['phone_number']}',"
            f"'{data['state_number']}',"
            f"'{5}'"
            ");")
        await cur.execute(query)
        await DB.conn.commit()
        await add_standart_rating(data['user_id'])


async def insert_new_loader(data):
    async with DB.conn.cursor() as cur:
        query = ("INSERT INTO loader VALUES("
            f"{data['user_id']},"
            f"'{data['name']}',"
            f"0,"
            f"'{data['phone_number']}'"
            ");")
        await cur.execute(query)
        await DB.conn.commit()


async def is_user_requested(id):
    async with DB.conn.cursor() as cur:
        query = ("SELECT count(1) "
                "FROM request "
                f"WHERE idrequest='{id}';")
        await cur.execute(query)
        result = (await cur.fetchall())[0][0]
    return bool(int(result))


async def is_user_registered(id):
    async with DB.conn.cursor() as cur:
        query = ("SELECT count(1) "
                "FROM kamaz "
                f"WHERE iduser='{id}';")
        await cur.execute(query)
        result1 = (await cur.fetchall())[0][0]
    async with DB.conn.cursor() as cur:
        query = ("SELECT count(1) "
                "FROM loader "
                f"WHERE iduser='{id}';")
        await cur.execute(query)
        result2 = (await cur.fetchall())[0][0]
    return bool(int(result1)) or bool(int(result2))


async def user_is_kamaz(id):
    async with DB.conn.cursor() as cur:
        query = ("SELECT count(1) "
                "FROM kamaz "
                f"WHERE iduser='{id}';")
        await cur.execute(query)
        result = (await cur.fetchall())[0][0]
    return bool(int(result))


async def user_is_loader(id):
    async with DB.conn.cursor() as cur:
        query = ("SELECT count(1) "
                "FROM loader "
                f"WHERE iduser='{id}';")
        await cur.execute(query)
        result = (await cur.fetchall())[0][0]
    return bool(int(result))


async def kamaz_change_status(user_id, status: int):
    async with DB.conn.cursor() as cur:
        query = (f"UPDATE kamaz SET idstatus={status} where iduser={user_id};")
        await cur.execute(query)
        await DB.conn.commit()


# Redis
async def add_standart_rating(user_id):
    count = 100
    rating_array = [5 for i in range(count)]
    await Redis.redis.hset(user_id, 'rating', json.dumps(rating_array))

