import logging

from aiogram import Router, F, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, LabeledPrice, PreCheckoutQuery, ContentType

from app.config import Config
from app.db.functions import User
from app.keyboards.inline import get_payment_keyboard
from app.states.user_states import UserStates

router = Router()


@router.callback_query(Text("replenish_balance"))
async def start_replenishing_the_balance(call: CallbackQuery, state: FSMContext):
    logging.info(f"Replenishment of the user's balance with telegram id {call.from_user.id} has been started")
    await call.answer(text="Пополнение баланса", show_alert=False)
    await call.message.edit_reply_markup(reply_markup=None)

    message = call.message
    await message.answer(
        "Введите сумму, на которую вы хотите пополнить баланс"
    )

    await state.set_state(UserStates.waiting_for_replenishment_amount)


@router.message(UserStates.waiting_for_replenishment_amount)
async def get_replenishment_amount(message: Message, state: FSMContext):
    replenishment_amount = message.text
    try:
        replenishment_amount = float(replenishment_amount)
    except ValueError:
        await message.answer(
            "Пожалуйста, отправьте боту число"
        )
        return

    logging.info(f"Received the amount of {replenishment_amount} rubles to replenish the user's balance "
                 f"(tg id: {message.chat.id})")
    await state.set_state(UserStates.waiting_for_pay)
    await send_payment_request_message(message, money_amount=replenishment_amount)


async def send_payment_request_message(message: Message, money_amount: float):
    await message.answer(
        f"Платеж успешно создан\n"
        f"Пополните баланс на {money_amount} р.",
        reply_markup=get_payment_keyboard(money_amount)
    )


@router.callback_query(F.data.startswith("pay"))
async def send_payment(call: CallbackQuery, state: FSMContext, bot: Bot, config: Config):
    await call.answer(text="Оплатите счет", show_alert=False)

    money_to_pay_amount = float(call.data.split("/")[1])
    price = LabeledPrice(label="Пополнение баланса", amount=money_to_pay_amount * 100)

    payment_message = await bot.send_invoice(
        chat_id=call.message.chat.id,
        title=f"Пополнение баланса",
        description="Пополнение баланса пользователя в боте @kerka_pay_bot",
        payload="test-invoice-payload",
        provider_token=config.payments.token,
        currency="rub",
        prices=[price],
    )

    logging.info(f"A message with an invoice for payment was sent to the user (tg id: {call.from_user.id})")
    await state.update_data(
        money_amount=money_to_pay_amount,
        payment_successful=False,
        payment_message=payment_message,
    )


@router.pre_checkout_query()
async def confirm_payment(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    logging.info(f"Payment bill confirmed (tg id: {pre_checkout_query.from_user.id})")


@router.message(UserStates.waiting_for_pay, F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message, state: FSMContext):
    await state.update_data(payment_successful=True)
    logging.info(f"Payment of user with id {message.from_user.id} was successful")


@router.callback_query(Text("check_payment"))
async def check_payment(call: CallbackQuery, state: FSMContext):
    await call.answer(text="Проверка платежа", show_alert=False)
    state_data = await state.get_data()

    money_amount = state_data.get("money_amount")
    payment_successful: bool = state_data.get("payment_successful")

    if payment_successful:
        await User.replenish_the_balance(amount=money_amount, telegram_id=call.from_user.id)
        logging.info(f"User with telegram id {call.from_user.id} replenished the balance by {money_amount} rubles")

        payment_message = state_data.get("payment_message")
        await payment_message.delete()
        await call.message.answer(
            f"Пополнение на сумму {money_amount} р.\n"
            f"прошло успешно!"
        )
        return

    await call.message.answer(
        f"Пополнение на сумму {money_amount} не прошло!\n"
        f"Пожалуйста, попробуйте еще раз"
    )
