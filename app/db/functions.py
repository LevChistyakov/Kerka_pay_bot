import logging

from tortoise.exceptions import DoesNotExist, IntegrityError

from app.db import models
from app.custom_exceptions.user_exceptions import UserAlreadyBanned


class User(models.User):

    @classmethod
    async def get_user(cls, telegram_id: int) -> models.User:
        return await cls.get(telegram_id=telegram_id)

    @classmethod
    async def is_registered(cls, telegram_id: int) -> bool:
        try:
            await cls.get_user(telegram_id)
            return True
        except DoesNotExist:
            return False

    @classmethod
    async def register(cls, telegram_id: int):
        await User(telegram_id=telegram_id).save()
        logging.info(f"User with telegram id {telegram_id} was registered")

    @classmethod
    async def replenish_the_balance(cls, amount: float, telegram_id: int):
        user: User = await cls.get_user(telegram_id)

        user.balance = user.balance + amount
        await user.save()

    @classmethod
    async def change_balance(cls, telegram_id: int, changed_balance: float):
        user: User = await cls.get_user(telegram_id)

        user.balance = changed_balance
        await user.save()

    @classmethod
    async def get_users(cls) -> list[models.User]:
        return await cls.all()


class BannedUser(models.BannedUser):

    @classmethod
    async def is_banned(cls, telegram_id: int, banned: set[int]) -> bool:
        return True if telegram_id in banned else False

    @classmethod
    async def ban_user(cls, telegram_id: int):
        try:
            await BannedUser(telegram_id=telegram_id).save()
        except IntegrityError:
            raise UserAlreadyBanned

    @classmethod
    async def get_all(cls):
        return await cls.all()
