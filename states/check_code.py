from aiogram.dispatcher.filters.state import StatesGroup, State


class CheckCode(StatesGroup):
    code = State()
