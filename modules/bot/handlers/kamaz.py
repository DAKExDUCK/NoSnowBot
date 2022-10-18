from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from modules.bot.functions.functions import get_rating
from modules.bot.keyboards.default import kamaz_btns

from modules.database.functions import kamaz_change_status

from ..functions.rights import IsKamaz, IsRegistered


async def change_status_active(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await kamaz_change_status(user_id, 1)
    await message.reply('Вы открыли смену!', reply_markup=kamaz_btns(1))


async def change_status_unactive(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await kamaz_change_status(user_id, 0)
    await message.reply('Вы закрыли смену!', reply_markup=kamaz_btns(0))


async def rating(message: types.Message, state: FSMContext):
    text = await get_rating(message.from_user.id)
    await message.reply(text)


def register_handlers_for_kamaz(dp: Dispatcher):
    dp.register_message_handler(
        change_status_active,
        IsRegistered(),
        IsKamaz(),
        lambda msg: msg.text == "Открыть смену",
        state="*"
    )
    dp.register_message_handler(
        change_status_unactive,
        IsRegistered(),
        IsKamaz(),
        lambda msg: msg.text == "Закрыть смену",
        state="*"
    )
    dp.register_message_handler(
        rating,
        IsRegistered(),
        IsKamaz(),
        commands='rating',
        state="*"
    )