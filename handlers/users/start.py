
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from loader import dp, bot
from states.check_code import CheckCode
from utils.db_api import db_commands as commands
from data.config import CHANNEL
from utils.misc import subscribtion

#Бот с поддержкой реферальной ссылки, входа с помощью пароля или через подписку на канал

@dp.message_handler(CommandStart())  #Фильтр на команду /start при первоночальном запуске бота
async def bot_start(message: types.Message):
    referral_args = message.get_args()   #В случае реферальной ссылки перехватываем код рефералла
    user = message.from_user.id
    user_in_db = await commands.select_user(user_id=message.from_user.id)  #Проверяем в базе ли пользователь

    if user_in_db:  #Если пользователь в базе
        await message.answer("Ты уже в базе, жми /menu")

    elif user != user_in_db and referral_args:  #Если не в базе и пришел через рефералльную сылку
        await commands.add_user_referral(user_id=message.from_user.id,      #Регистрируем бользователя в базе через реферальную ссылку
                                         full_name=message.from_user.full_name,
                                         username=message.from_user.username,
                                         referrer_id=referral_args)
        referral_args = message.get_args()
        await commands.add_referral_money(referrer_id=referral_args)  #Так же добавляем деньги человеку, который привел пользователя
        await message.answer(
                "\n".join(
                    [
                        f"Привет, {message.from_user.full_name} !",
                        f"Теперь жми /menu !"
                    ]
                )
            )

    elif user != user_in_db:  #Если пользователь не в базе и без реферальной ссылки
        chat = await bot.get_chat(CHANNEL)   #Берем канал на который надо подписаться для доступа к боту
        invite_link = await chat.export_invite_link()
        channel_format = f'Канал {invite_link}'  #Ссылка на канал для подписки
        await message.answer(f"Привет! Чтобы воспользоваться ботом необходимо совершить одно из действий ниже: "
                             f"\n1)Ввести код приглашения (просто напишите его боту) \n2) Воспользоваться реферальной ссылкой"
                             f"\n3) Подписаться на канал: \n{channel_format}")
        status = await subscribtion.check( user_id=message.from_user.id,
                                           channel=CHANNEL )  #Проверяем подписку на канал

        if status:   #Если подписался то заносим в базу
            await commands.add_user( user_id=message.from_user.id,
                                     full_name=message.from_user.full_name,
                                     username=message.from_user.username )
            await message.answer( 'Отлично! Теперь жми /menu !' )
        await CheckCode.code.set()   #Вводим в состояние на случай доступа через пароль

    @dp.message_handler(state=CheckCode.code)
    async def get_checking_code(mess: types.Message, state: FSMContext):
            code = mess.text
            if code == "111":
                await commands.add_user( user_id=message.from_user.id,
                                         full_name=message.from_user.full_name,
                                         username=message.from_user.username )
                await mess.answer( 'Отлично! Теперь жми /menu !' )
            await state.finish()






