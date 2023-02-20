import logging

from aiogram import Router, Bot
from aiogram.filters import Text
from aiogram.types import CallbackQuery, FSInputFile

from app.db.functions import User
from app.db import models
from app.files.csv_logic import CsvFile

router = Router()


@router.callback_query(Text("get_users"))
async def send_users(call: CallbackQuery, bot: Bot):
    users: list[models.User] = await User.get_users()
    logging.info("Received information about users and their balances from database")

    users_file = CsvFile(file_name="users.csv")
    users_file.create_table_from_query_result(users)
    logging.info("A file about users and their balances was created")

    await bot.send_document(
        call.message.chat.id,
        document=FSInputFile(users_file.path_to_file),
        caption="Данные о пользователях и их балансах"
    )
    logging.info("A file about users and their balances was sended")
