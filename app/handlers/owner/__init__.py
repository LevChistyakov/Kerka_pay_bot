from aiogram import Router

from . import get_users, admin_home, get_logs, edit_user_balance, ban_user


def get_owner_router() -> Router:
    router = Router()
    router.include_router(admin_home.router)
    router.include_router(get_users.router)
    router.include_router(get_logs.router)
    router.include_router(edit_user_balance.router)
    router.include_router(ban_user.router)

    return router
