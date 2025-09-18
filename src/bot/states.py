from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    add_category = State()
    subscribed = State()
