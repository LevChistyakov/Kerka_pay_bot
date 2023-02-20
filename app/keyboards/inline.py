from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_replenish_balance_keyboard() -> InlineKeyboardMarkup:
    button = InlineKeyboardButton(text="Пополнить баланс", callback_data="replenish_balance")

    keyboard = InlineKeyboardBuilder(markup=[
        [button]
    ])

    return keyboard.as_markup()


def get_payment_keyboard(money_amount: float) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Оплатить", callback_data=f"pay/{money_amount}")],
        [InlineKeyboardButton(text="Проверить платеж", callback_data=f"check_payment")]
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    return keyboard.as_markup()


def get_admin_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Получить список пользователей с балансами", callback_data=f"get_users")],
        [InlineKeyboardButton(text="Получить логи", callback_data=f"get_logs")],
        [InlineKeyboardButton(text="Изменить баланс пользователя", callback_data=f"edit_user_balance")],
        [InlineKeyboardButton(text="Заблокировать пользователя", callback_data=f"ban_user")],

    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    return keyboard.as_markup()


def get_logs_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Стандартные логи", callback_data="get_default_logs")],
        [InlineKeyboardButton(text="Логи ошибок", callback_data="get_errors_logs")]
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    return keyboard.as_markup()
