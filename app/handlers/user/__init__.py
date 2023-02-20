from aiogram import Router

from . import start, replenish_balance


def get_user_router() -> Router:
    router = Router()
    router.include_router(start.router)
    router.include_router(replenish_balance.router)

    return router
