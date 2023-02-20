import logging

from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.db.functions import User
from app.handlers.owner.utils import try_to_get_user_id_from_message_text
from app.states.owner_states import EditUserBalanceStates

router = Router()


@router.callback_query(Text("edit_user_balance"))
async def start_editing_user_balance(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        "Отправьте мне id или перешлите сообщение от пользователя, для которого необходимо изменить баланс"
    )
    await state.set_state(EditUserBalanceStates.waiting_for_user_id)


@router.message(EditUserBalanceStates.waiting_for_user_id)
async def try_to_get_user_id(message: Message, state: FSMContext):
    try:
        user_id = message.forward_from.id
    except AttributeError:
        user_id = await try_to_get_user_id_from_message_text(message)
        if user_id is None:
            return
    logging.info(f"Got telegram id to change balance = {user_id}")

    user_exist = await User.is_registered(telegram_id=user_id)
    if user_exist:
        await request_new_balance(message, user_id, state)
        return

    logging.info(f"User with telegram id = {user_id} was not registered")
    await message.answer("Пользователь с данным id не зарегистрирован в боте!")


async def request_new_balance(message: Message, user_id: int, state: FSMContext):
    await state.update_data(user_id=user_id)
    await message.answer(
        "Отправьте измененнный баланс"
    )
    await state.set_state(EditUserBalanceStates.waiting_for_new_balance)


@router.message(EditUserBalanceStates.waiting_for_new_balance)
async def get_new_balance(message: Message, state: FSMContext):
    try:
        new_balance = float(message.text)
    except ValueError:
        await message.answer(
            "Баланс должен быть числом!"
        )
        return

    state_data = await state.get_data()
    user_id = state_data.get("user_id")
    logging.info(f"Amended balance received = {new_balance} rubles (user tg id: {user_id})")

    await User.change_balance(user_id, changed_balance=new_balance)
    logging.info(f"User balance was changed to {new_balance} rubles (user tg id: {user_id})")
    await message.answer(
        "Баланс пользователя успешно изменен!"
    )
