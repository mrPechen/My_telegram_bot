from aiogram import types
from data.config import TOKEN
from keyboards.inline.menu_keyboards import buy_item_menu
from loader import dp, bot
from utils.db_api.db_commands import get_item, save_purchase, check_balance

#Обрабатываем кнопку "купить"
@dp.callback_query_handler(buy_item_menu.filter())
async def show_invoices(call: types.CallbackQuery, callback_data: dict):
    item_id = callback_data.get("item_id")
    item = await get_item(item_id=item_id)
    balance = await check_balance(user_id=call.from_user.id)
    update_balance = int(item.price) - balance

    await bot.send_invoice(chat_id=call.from_user.id,
                           title=f"{item.name}",
                           description=f"{item.description}",
                           start_parameter="create_invoice",
                           payload=f"{item.name}",
                           provider_token=TOKEN,
                           currency="RUB",
                           prices=[
                               types.LabeledPrice(
                                   label=f"{item.name}",
                                   amount=int(update_balance)
                               )
                           ],
                           photo_url=f"{item.photo}",
                           need_name=True,
                           need_phone_number=True,
                           need_shipping_address=True,

                           )

#Решестрируем заказ в базе
@dp.pre_checkout_query_handler()
async def register_pre_check(pre_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_query.id, ok=True)
    await save_purchase(user_id=pre_query.from_user.id, phone_number=pre_query.order_info.phone_number,
                        shipping_address=pre_query.order_info.shipping_address, item=pre_query.invoice_payload,
                        amount=pre_query.total_amount, quantity="1", receiver=pre_query.order_info.name)
    await bot.send_message(chat_id="300645955", text="Поступил новый заказ. Вот информация:"
                                                      f"\nТовар: {pre_query.invoice_payload}"
                                                      f"\nЗаказчик: {pre_query.order_info.name}")





