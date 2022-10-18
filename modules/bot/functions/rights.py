from aiogram.dispatcher.filters import Filter
from aiogram import types

from ...database.functions import is_user_registered, is_user_requested, user_is_kamaz, user_is_loader

admin_list = [626591599]


class IsAdmin(Filter):
    key = "is_admin"

    async def check(self, message: types.Message):
        return message.from_user.id in admin_list
        


class IsRegistered(Filter):
    key = "is_registered"

    async def check(self, message: types.Message):
        return await is_user_registered(message.from_user.id)


class IsRequested(Filter):
    key = "is_requested"

    async def check(self, message: types.Message):
        return await is_user_requested(message.from_user.id)


class IsKamaz(Filter):
    key = "is_kamaz"

    async def check(self, message: types.Message):
        return await user_is_kamaz(message.from_user.id)


class IsLoader(Filter):
    key = "is_loader"

    async def check(self, message: types.Message):
        return await user_is_loader(message.from_user.id)
