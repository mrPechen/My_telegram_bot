from aiogram.dispatcher.filters.state import StatesGroup, State


class GetItem(StatesGroup):
    item_id = State()
