from aiogram import Bot


async def check(user_id, channel):
    bot = Bot.get_current()
    member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
    return member.is_chat_member()
