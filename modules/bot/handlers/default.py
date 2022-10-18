from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove

from ...database.functions import insert_new_request
from ..functions.functions import send_request_to_admin
from ..functions.rights import IsRegistered, IsRequested
from ..handlers.logger import log_msg, logger
from ..keyboards.default import (agree_restart_btns, name_kb, phone_number_kb,
                                 register_menu_btns, role_kb)


class Form(StatesGroup):
    wait_choose_role = State()
    wait_name = State()
    wait_state_number = State()
    wait_phone_number = State()


async def menu(message: types.Message, state: FSMContext):
    await message.reply('Меню')


async def just_wait(message: types.Message, state: FSMContext):
    await message.reply('Пожалуйста, подождите, Ваша заявка еще не рассмотрена!')


async def start(message: types.Message, state: FSMContext):
    text = "Привет! Я NoSnow Бот"
    await message.reply(text, reply_markup=register_menu_btns())
    await Form.wait_choose_role.set()


async def register(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=None)
    text = "Выбери свою роль:"
    await query.message.answer(text, reply_markup=role_kb())
    await Form.wait_choose_role.set()


async def set_role(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Погрузчик':
            data['role'] = 0
            data['state_number'] = ''
        elif message.text == 'Камаз':
            data['role'] = 1
        else:
            return
    text = "Как мне тебя звать?"
    await message.reply(text, reply_markup=name_kb(message.from_user.full_name))
    await Form.wait_name.set()


async def set_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    
    if data['role'] == 0:
        text = "Теперь отправь мне свой номер телефона"
        await message.reply(text, reply_markup=phone_number_kb())
        await Form.wait_phone_number.set()
    else:
        text = "Теперь отправь гос. номер твоего авто"
        await message.reply(text, reply_markup=ReplyKeyboardRemove())
        await Form.wait_state_number.set()


async def set_state_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state_number'] = message.text
    text = "Теперь отправь мне свой номер телефона"
    await message.reply(text, reply_markup=phone_number_kb())
    await Form.wait_phone_number.set()


async def set_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.contact:
            data['user_id'] = message.from_user.id
            data['phone_number'] = message.contact['phone_number']
        else:
            data['phone_number'] = message.text

    text = f"Ваши данные:\n\n" \
            f"Имя: {data['name']}\n" \
            f"Номер телефона: {data['phone_number']}\n"
    if data['role'] == 0:
        text+= f"Авто: Погрузчик"
    else:
        text+= f"Авто: Камаз\n"
        text+= f"Гос. номер: {data['state_number']}"
        
    await message.reply(text, reply_markup=agree_restart_btns())


async def agree_form(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        try:
            await insert_new_request(data.as_dict())
            await send_request_to_admin(data.as_dict())
        except Exception as exc:
            logger.exception(f"{query.from_user.id} {query.data}", exc_info=True)
            text = "Ошибка!"
            await query.answer(text)
        else:
            await query.message.edit_reply_markup(reply_markup=None)
            text = "Успех! Ваша заявка отправлена на проверку к Админу"
            await query.message.answer(text)
            await state.finish()


async def restart_form(query: types.CallbackQuery, state: FSMContext):
    text = "Выбери свою роль:"
    await query.message.answer(text, reply_markup=role_kb())
    await state.finish()
    await Form.wait_choose_role.set()


async def delete_msg(query: types.CallbackQuery, state: FSMContext):
    try:
        await query.bot.delete_message(query.message.chat.id, query.message.message_id)
        if query.message.reply_to_message:
            await query.bot.delete_message(query.message.chat.id, query.message.reply_to_message.message_id)
        await query.answer()
    except Exception as exc:
        logger.error(exc)
        await query.answer("Error")


def register_handlers_default(dp: Dispatcher):
    dp.register_message_handler(
        just_wait,
        IsRequested(),
        commands="start",
        state="*"
    )
    dp.register_message_handler(
        menu,
        IsRegistered(),
        commands="start",
        state="*"
    )
    dp.register_message_handler(
        start,
        commands="start",
        state="*"
    )
    dp.register_callback_query_handler(
        register,
        lambda c: c.data == "register",
        state="*"
    )

    dp.register_message_handler(
        set_role,
        lambda msg: msg.text in ['Погрузчик', 'Камаз'],
        content_types=['text'],
        state=Form.wait_choose_role
    )
    dp.register_message_handler(
        set_name,
        content_types=['text'],
        state=Form.wait_name
    )
    dp.register_message_handler(
        set_state_number,
        content_types=['text'],
        state=Form.wait_state_number
    )
    dp.register_message_handler(
        set_phone_number,
        content_types=['text', 'contact'],
        state=Form.wait_phone_number
    )
    dp.register_callback_query_handler(
        agree_form,
        lambda c: c.data == "agree_form",
        state="*"
    )
    dp.register_callback_query_handler(
        restart_form,
        lambda c: c.data == "restart_form",
        state="*"
    )


    dp.register_callback_query_handler(
        delete_msg,
        lambda c: c.data == "delete",
        state="*"
    )
