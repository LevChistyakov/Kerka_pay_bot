from typing import Optional

from aiogram.types import Message


async def try_to_get_user_id_from_message_text(message: Message) -> Optional[int]:
    try:
        user_id = int(message.text)
    except ValueError:
        await message.answer(
            "id пользователя должен состоять только из цифр!"
        )
        return
    return user_id
