import logging
import os

from aiogram import Router, Bot
from aiogram.filters import Text
from aiogram.types import CallbackQuery, FSInputFile

from app.keyboards.inline import get_logs_keyboard

router = Router()


@router.callback_query(Text("get_logs"))
async def start_sending_logs(call: CallbackQuery):
    await call.message.answer(
        "Какие именно логи вы хотите получить?",
        reply_markup=get_logs_keyboard()
    )


@router.callback_query(Text("get_default_logs"))
async def send_default_logs(call: CallbackQuery, bot: Bot):
    logging.info("Started sending default logs")
    await bot.send_document(
        call.message.chat.id,
        document=FSInputFile(os.path.join("log_files", "default.log")),
        caption="Стандартные логи"
    )
    logging.info("Default logs have been sent")


@router.callback_query(Text("get_errors_logs"))
async def send_errors_logs(call: CallbackQuery, bot: Bot):
    logging.info("Started sending errors logs")
    await bot.send_document(
        call.message.chat.id,
        document=FSInputFile(os.path.join("log_files", "errors.log")),
        caption="Логи ошибок"
    )
    logging.info("Errors logs have been sent")
