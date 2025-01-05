from aiogram.dispatcher.filters.state import StatesGroup, State


class UserAnketa(StatesGroup):
    add_fullname = State()
    add_phone = State()
