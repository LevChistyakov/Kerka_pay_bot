from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    waiting_for_replenishment_amount = State()
    waiting_for_pay = State()
