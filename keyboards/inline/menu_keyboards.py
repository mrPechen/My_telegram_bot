from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import bot
from utils.db_api.db_commands import get_item
start_menu = CallbackData("start_menu", "key")
buy_item_menu = CallbackData("buy", "item_id")
referrals_menu = CallbackData("referrals_menu", "key")
balance_menu = CallbackData("balance_menu", "key")
get_item_call = CallbackData("get_item", "key")

#Меню для пользователя
def menu_user():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(
        InlineKeyboardButton(
            text="Товары",
            switch_inline_query_current_chat=""
        )),
    markup.insert(
        InlineKeyboardButton(
            text="Ваш баланс",
            callback_data=balance_menu.new(key="balance")
        )
    ),
    markup.insert(
        InlineKeyboardButton(
            text="Реферальная система",
            callback_data=start_menu.new(key="referral_menu")

        ))

    return markup

#Меню для админа
def menu_admin():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(
        InlineKeyboardButton(
            text="Товары",
            switch_inline_query_current_chat=""
        )),
    markup.insert(
        InlineKeyboardButton(
            text="Ваш баланс",
            callback_data=balance_menu.new(key="balance")
        )),
    markup.insert(
        InlineKeyboardButton(
            text="Рефералальная система",
            callback_data=start_menu.new(key="referral_menu")
        )),
    markup.insert(
        InlineKeyboardButton(
            text="Админка", url="http://0.0.0.0:8000/admin",
            callback_data=start_menu.new(key="admin")
        ))

    return markup

#Реферальное меню
def referral_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(
        InlineKeyboardButton(
            text="Мои рефералы", callback_data=referrals_menu.new(key="my_referrals")
            )
        )
    markup.insert(
        InlineKeyboardButton(
            text="Моя реферальная ссылка",
            callback_data=referrals_menu.new(key="referrer_url")
        )
    )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=start_menu.new(key='back_from_referrals_menu')
        )
    )
    return markup

#Кнопка выбрать товар
async def get_item_func(item_id):
    markup = InlineKeyboardMarkup()
    bot_username = (await bot.me).username
    item = await get_item(item_id)
    button_text = "Показать товар"
    markup.insert(InlineKeyboardButton(
            text=button_text,
            switch_inline_query_current_chat=f"{item.id}",
            url=f"https://t.me/{bot_username}?start=i{item.id}"
    ))

    return markup

#Кнопка показать инфо о товаре
async def full_info_item(item_id):
    markup = InlineKeyboardMarkup()
    button_text = f"Купить"
    markup.insert(
        InlineKeyboardButton(
            text=button_text,
            callback_data=buy_item_menu.new(item_id=item_id)
        )
    )
    return markup

