from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.filters.is_owner import IsOwner
from app.keyboards.inline import get_admin_keyboard

router = Router()


@router.message(IsOwner(is_owner=True), Command('admin'))
async def select_action(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Здравствуйте, выберите действие",
        reply_markup=get_admin_keyboard()
    )
