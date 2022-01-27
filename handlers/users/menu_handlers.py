import re

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputMessageContent

from keyboards.inline.menu_keyboards import menu_admin, menu_user, get_item_func, full_info_item
from loader import dp
from states.get_item import GetItem
from utils.db_api.db_commands import search_item, select_user, get_item

#Обработка команды /menu
@dp.message_handler(commands='menu')
async def menu_categories(message: Message):
    user = message.from_user.id
    if user == 300645955 or 362089194:
        await message.answer(text="hi admin", reply_markup=menu_admin())
    else:
        await message.answer(text=f"Что желаешь {message.from_user.username}?", reply_markup=menu_user())

#Обработка кнопки Товары
@dp.inline_handler()
async def get_items(query: InlineQuery):
    user_in_db = await select_user(user_id=query.from_user.id)
    if user_in_db: #Если юзер в базе то товары будут показаны с помощью инлайн режима
        items_list = await search_item(search_query=query.query or None)
        await query.answer(results=[
            InlineQueryResultArticle(
                id=item.id,
                title=f"{item.name} - {item.price}",
                thumb_url=f"{item.photo}",
                input_message_content=InputMessageContent(message_text=f"{item.id}"),
                hide_url=True,

                ) for item in items_list], is_personal=True)
        await GetItem.item_id.set()  #Закидываем в состояние для отслеживания выбранного товара

#Обработка выбранного товара
#После нажатии кнопки "Товары" и поиска товаров, если это все отменить, то состояние ожидает id товара и при команде /menu выдает ошибку. Поэтому пробуем через try/except
@dp.message_handler(state=GetItem.item_id)
async def show_item(message: Message, state: FSMContext):
    try:
        item_id = message.text
        item = await get_item(item_id=item_id)
        markup = await get_item_func(item_id=item_id)
        await message.answer(text=f"{item_id}")
        await message.answer_photo(photo=f"{item.photo}", caption=f"Вы выбрали {item.name} - {item.price}$"
                                                              f"\nНазад - /menu", reply_markup=markup)
        await state.reset_state()
    except Exception:
        pass

#Обрабатываем кнопку "показать инфо о товаре".
#Так как мы открываем эту кнопку через ссылку, то ссылка пересекается с функцией /start, которая используется для занесения пользователя в базу здесь фильтруем старт через deeplink и рег. выражения
@dp.message_handler(CommandStart(deep_link=re.compile(r"^i[0-9]{1,2}$")))
async def show_full_info_item(message: Message):
    item_id = message.get_args()[1]
    item = await get_item(item_id=item_id)
    markup = await full_info_item(item_id=item_id)
    await message.answer_photo(photo=f"{item.photo}",
                                   caption=f"{item.name} - {item.price}$\n{item.description}\nНазад - /menu",
                                   reply_markup=markup)

