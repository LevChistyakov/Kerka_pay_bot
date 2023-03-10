from aiogram import Router
from .user import get_user_router
from .owner import get_owner_router


def get_handlers_router() -> Router:
    router = Router()

    user_router = get_user_router()
    owner_router = get_owner_router()

    router.include_router(user_router)
    router.include_router(owner_router)

    return router
