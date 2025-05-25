from TelegramBot.keyboards.main import get_menu_kb

from aiogram import Router
from aiogram.types import Message

default_router = Router()

@default_router.message()
async def default_handler(message: Message) -> None:
    await message.answer('Извините, я не говорю по-русски.', )
                        #  reply_markup=get_menu_kb()) 