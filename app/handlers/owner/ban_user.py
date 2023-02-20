import logging

from aiogram import Router, Dispatcher
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.config import Config
from app.db.functions import BannedUser, User
from app.handlers.owner.utils import try_to_get_user_id_from_message_text
from app.middlewares.banned_users_middleware import register_banned_users_middleware
from app.states.owner_states import BanUserStates
from app.custom_exceptions.user_exceptions import UserAlreadyBanned

router = Router()


@router.callback_query(Text("ban_user"))
async def start_editing_user_balance(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        "Отправьте мне id или перешлите сообщение от пользователя, которого необходимо заблокировать"
    )
    await state.set_state(BanUserStates.waiting_for_user_id)


@router.message(BanUserStates.waiting_for_user_id)
async def try_to_ban_user_by_id(message: Message, dp: Dispatcher, config: Config):
    try:
        user_id = message.forward_from.id
    except AttributeError:
        user_id = await try_to_get_user_id_from_message_text(message)
        if user_id is None:
            return
    logging.info(f"Got telegram id to block = {user_id}")

    if user_id == config.settings.owner_id:
        await message.answer(
            "Нельзя заблокировать админа!"
        )
        return

    user_exist = await User.is_registered(telegram_id=user_id)
    if user_exist:
        logging.info(f"Try to ban user with telegram id {user_id}")
        await try_to_ban_user(message, user_id, dp)
        return

    logging.info(f"User with telegram id = {user_id} was not registered")
    await message.answer("Пользователь с данным id не зарегистрирован в боте!")


async def try_to_ban_user(message: Message, user_id: int, dp: Dispatcher):
    try:
        await BannedUser.ban_user(telegram_id=user_id)
    except UserAlreadyBanned:
        await message.answer(
            "Данный пользователь уже заблокирован!"
        )
        return

    logging.info(f"User with telegram id {user_id} was banned")
    await register_banned_users_middleware(dp)
    await message.answer(
        f"Пользователь с id {user_id} был успешно заблокирован!"
    )
