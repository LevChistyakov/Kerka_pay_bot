from aiogram.fsm.state import State, StatesGroup


class BanUserStates(StatesGroup):
    waiting_for_user_id = State()


class EditUserBalanceStates(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_new_balance = State()
