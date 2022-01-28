from aiogram.types import CallbackQuery

from keyboards.inline.menu_keyboards import referrals_menu, referral_menu, start_menu, menu_user, menu_admin
from loader import dp, bot
from utils.db_api.db_commands import check_referrals, get_id

#Обработка кнопки рерального меню
@dp.callback_query_handler(start_menu.filter(key="referral_menu"))
async def get_referral_menu(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=referral_menu())

#Обработка кнопки "мои рефералы"
@dp.callback_query_handler(referrals_menu.filter(key="my_referrals"))
async def get_my_referrals(call: CallbackQuery):
    user_id = call.from_user.id
    referrals = await check_referrals(user_id=user_id)
    text = ""
    for referral in referrals:
        text += str(referral)
    await call.message.answer(text=f"Ваши рефералы:\n" + text)

#Обработка кнопки "моя реферальная ссылка"
@dp.callback_query_handler(referrals_menu.filter(key="referrer_url"))
async def get_my_referrals_url(call: CallbackQuery):
    user_id = call.from_user.id
    bot_username = (await bot.me).username
    id = await get_id(user_id)
    referral_link = f"https://t.me/{bot_username}?start={id}"
    text = f"Ваша реферальная ссылка: {referral_link}"
    await bot.send_message(user_id, text)

#Обработка кнопки домой
@dp.callback_query_handler(start_menu.filter(key="back_from_referrals_menu"))
async def back_to_menu(call: CallbackQuery):
    markup_user = menu_user()
    markup_admin = menu_admin()
    user = call.from_user.id
    if user == #User ID телеграм:
        await call.message.edit_reply_markup(markup_admin)
    else:
        await call.message.edit_reply_markup(markup_user)


