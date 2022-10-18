import json
import os

import dotenv
from aiogram import Bot

dotenv.load_dotenv()

SQL_HOST = os.getenv('SQL_HOST') 
SQL_PORT = os.getenv('SQL_PORT') 
SQL_USER = os.getenv('SQL_USER_DB') 
SQL_PASSWD = os.getenv('SQL_PASSWD') 
SQL_DB = os.getenv('SQL_DB') 

REDIS_HOST = os.getenv('REDIS_HOST') 
REDIS_PORT = os.getenv('REDIS_PORT') 
REDIS_USER = os.getenv('REDIS_USER_DB') 
REDIS_PASSWD = os.getenv('REDIS_PASSWD') 
REDIS_DB = os.getenv('REDIS_DB') 

with open('logs.log', 'w+') as f:
    ...
with open('debug.log', 'w+') as f:
    ...
with open('log_config.json', 'r') as f:
    log_config = json.load(f)

bot = Bot(token=os.getenv('TOKEN'), parse_mode='HTML')
