from aiogram import Dispatcher

from . import banned_users_middleware


async def register_middlewares(dp: Dispatcher):
    await banned_users_middleware.register_banned_users_middleware(dp)
