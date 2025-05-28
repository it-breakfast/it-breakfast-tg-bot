from TelegramBot.keyboards.main import get_menu_kb

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

default_router = Router()

@default_router.message(CommandStart())
async def default_handler(message: Message) -> None:
    await message.answer('Извините, я не говорю по-русски.', )
                        #  reply_markup=get_menu_kb()) 

# @default_router.message(CommandStart())
# async def cmd_start(message: Message):
#     await message.answer('Запуск сообщения по команде /start используя фильтр CommandStart()')

# @default_router.message(Command('start_2'))
# async def cmd_start_2(message: Message):
#     await message.answer('Запуск сообщения по команде /start_2 используя фильтр Command()')

# @default_router.message(F.text == '/start_3')
# async def cmd_start_3(message: Message):
#     await message.answer('Запуск сообщения по команде /start_3 используя магический фильтр F.text!')
