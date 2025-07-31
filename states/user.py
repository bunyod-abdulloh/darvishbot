from aiogram.dispatcher.filters.state import StatesGroup, State


class UserAnketa(StatesGroup):
    add_fullname = State()
    add_phone = State()
    GET_AGE = State()
    FULL_NAME = State()
    WORK = State()
    EEG = State()
    PHONE = State()
