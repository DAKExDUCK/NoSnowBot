from email import message
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from modules.bot.keyboards.default import kamaz_btns

from ...database.functions import (delete_request, get_request, insert_new_kamaz,
                              insert_new_loader)
from ..functions.rights import IsAdmin


async def start_admin(message: types.Message, state: FSMContext):
    await message.reply('start message for admin')


async def send_log(message: types.Message, state: FSMContext):
    with open('logs.log', 'r') as logs:
        await message.reply_document(logs)


async def accept_request(query: types.CallbackQuery, state: FSMContext):
    accept_bool = bool(int(query.data.split('|')[2]))
    id = query.data.split('|')[3]
    if accept_bool:
        data = await get_request(id)
        await delete_request(id)
        if data['role']:
            await insert_new_kamaz(data)
            kb = kamaz_btns(0)
        else:
            await insert_new_loader(data)
            kb = None
        await query.answer('Пользователь добавлен!')
        await query.message.delete()
        text = 'Ваша заявка была одобрена!'
    else:
        await delete_request(id)
        await query.answer('Пользователь отклонен!')
        await query.message.delete()
        text = 'Ваша заявка была отклонена!'
        kb = None

    await query.bot.send_message(id, text, reply_markup=kb)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(start_admin, IsAdmin(), commands="start", state="*")
    dp.register_message_handler(send_log, IsAdmin(), commands="get_logfile", state="*")

    dp.register_callback_query_handler(
        accept_request,
        lambda c: c.data.split('|')[0] == "request" and 
                    c.data.split('|')[1] == 'accept',
        state="*"
    )
    