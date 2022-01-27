from aiogram.types import CallbackQuery

from keyboards.inline.menu_keyboards import balance_menu
from loader import dp
from utils.db_api.db_commands import check_balance

#Обрабатываем кнопку "баланс"
@dp.callback_query_handler(balance_menu.filter(key="balance"))
async def get_balance(call: CallbackQuery):
    user_id = call.from_user.id
    balance = await check_balance(user_id=user_id)
    await call.message.answer(text="Ваш баланс: " + str(balance))
