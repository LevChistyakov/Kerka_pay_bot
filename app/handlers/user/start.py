import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.db.functions import User
from app.keyboards.inline import get_replenish_balance_keyboard

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    logging.info(f"User with telegram id {message.from_user.id} started the bot")
    await state.clear()

    user_id = message.from_user.id
    name = message.from_user.first_name

    if not await User.is_registered(user_id):
        await User.register(user_id)
    await message.answer(
        f"Привет, {name}\n\n"
        f"Я - бот для пополнения баланса.\n"
        f"Нажмите на кнопку, чтобы пополнить баланс",
        reply_markup=get_replenish_balance_keyboard()
    )
