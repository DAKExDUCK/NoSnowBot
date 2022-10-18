import json
import random
from modules.bot.keyboards.default import accept_request_btns
from config import bot
from modules.database.main import Redis
from ..functions.rights import admin_list


async def send_request_to_admin(data):
    admin_id = random.choice(admin_list)
    text = f"Новая заявка:\n\n"
    if data['role']:
        text += f"{data['name']} - Камаз\n" \
                f"{data['phone_number']}\n" \
                f"{data['state_number']}"
    else:
        text += f"{data['name']} - Погрузчик\n" \
                f"{data['phone_number']}"
    
    await bot.send_message(admin_id, text, reply_markup=accept_request_btns(data['user_id']))


async def get_rating(user_id):
    arr = json.loads(await Redis.redis.hget(user_id, 'rating'))
    count_weight = 10
    arr = arr[:count_weight]
    
    divisible = 0
    if len(arr) > count_weight:
        divider = (count_weight * (count_weight+1))/2
    else:
        divider = (len(arr) * (len(arr)+1))/2

    score = count_weight
    for i in range(0, count_weight):
        if i >= len(arr):
            continue
        divisible += arr[i]*(score)
        print(arr[i], (score))
        score -= 1
    
    return divisible/divider
