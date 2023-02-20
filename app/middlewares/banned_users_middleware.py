from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Update, Message, CallbackQuery

from app.db import models
from app.db.functions import BannedUser


class BannedUsersMiddleware(BaseMiddleware):

    def __init__(self, banned_users_ids):
        self.banned_users_ids: set[int] = banned_users_ids

    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any],
    ) -> Any:
        user_banned = await BannedUser.is_banned(
            telegram_id=event.from_user.id,
            banned=self.banned_users_ids
        )

        if user_banned:
            return
        return await handler(event, data)


async def register_banned_users_middleware(dp: Dispatcher):
    banned_users: list[models.BannedUser] = await BannedUser.get_all()
    banned_ids: set[models.BannedUser.telegram_id] = {user.telegram_id for user in banned_users}

    banned_users_middleware = BannedUsersMiddleware(banned_users_ids=banned_ids)

    dp.message.middleware(banned_users_middleware)
    dp.callback_query.middleware(banned_users_middleware)
