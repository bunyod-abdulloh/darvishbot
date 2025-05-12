from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminState(StatesGroup):
    are_you_sure = State()
    ask = State()
    send_to_users = State()
    yaxinquestions = State()
    yaxinscales = State()
    leoquestions = State()
    leoscales = State()
    ayzquestions = State()
    ayzscales = State()
