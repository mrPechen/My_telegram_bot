from aiogram.dispatcher.filters.state import StatesGroup, State


class BuyItem(StatesGroup):
    purchase = State()
    item = State()
