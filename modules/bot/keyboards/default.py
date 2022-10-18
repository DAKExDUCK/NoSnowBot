from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)


def register_menu_btns():
    btn_agree = InlineKeyboardButton('Регистрация', callback_data=f'register')

    kb = InlineKeyboardMarkup()
    kb.add(btn_agree)

    return kb


def role_kb():
    btn_loader = KeyboardButton('Погрузчик')
    btn_kamaz = KeyboardButton('Камаз')

    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(btn_loader, btn_kamaz)

    return kb


def name_kb(name:str = None):
    if name is None:
        return None

    btn_phone_number = KeyboardButton(name, one_time_keyboard=True)

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(btn_phone_number)

    return kb


def phone_number_kb():
    btn_phone_number = KeyboardButton('Отправить номер телефона', request_contact=True)

    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(btn_phone_number)

    return kb


def agree_restart_btns():
    btn_agree = InlineKeyboardButton('Отправить', callback_data='agree_form')
    btn_restart = InlineKeyboardButton('Заполнить заново', callback_data='restart_form')

    kb = InlineKeyboardMarkup()
    kb.row(btn_agree, btn_restart)

    return kb


def accept_request_btns(id):
    btn_agree = InlineKeyboardButton('Принять', callback_data=f'request|accept|1|{id}')
    btn_cancel = InlineKeyboardButton('Отклонить', callback_data=f'request|accept|0|{id}')

    kb = InlineKeyboardMarkup()
    kb.row(btn_agree, btn_cancel)

    return kb


def kamaz_btns(status):
    if status == 0:
        btn_smena = KeyboardButton('Открыть смену')
    elif status == 1:
        btn_smena = KeyboardButton('Закрыть смену')
    elif status == 2:
        btn_smena = KeyboardButton('Закончить обьект')

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(btn_smena)

    return kb
    