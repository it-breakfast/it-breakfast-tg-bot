import asyncio
from datetime import datetime

from TelegramBot.keyboards.main import get_menu_kb
from TelegramBot.helpers.cron import message_state
from TelegramBot.logging import LOGGER

from aiogram import Bot
from aiogram import Router, F
from aiogram.types import (
    Message, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, PreCheckoutQuery,
    
)
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BufferedInputFile

from TelegramBot.helpers.admin_filter import IsAdmin
from TelegramBot.config import ADMINS, CHAT_ID

import re
import io
import qrcode

default_router = Router()
message_time_router = Router()
pre_checkout_failed_reason = "Что-то пошло не так. Нет больше места для денег 😭"
pre_checkout_ok_reason = "Ваши денежки у нас"

@message_time_router.message()
async def save_message_time(message: Message) -> None:
    """
    Сохраняет время последнего сообщения в чате.
    """
    message_state.last_message_time = message.date
    LOGGER(__name__).info(f"Сохранено время последнего сообщения: {message.date}")

default_router.include_router(message_time_router)

@default_router.message(CommandStart())
async def default_handler(message: Message) -> None:
    await message.answer('Извините, я не говорю по-русски.', )

@default_router.message(Command('test_k'))
async def cmd_start_2(message: Message):
    button = InlineKeyboardButton(text="Test", callback_data="test_me")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await message.reply("Just a test", reply_markup=keyboard)

@default_router.message(Command('qr'))
async def cmd_qr(message: Message):
    if not message.reply_to_message is not None:
        return message.reply(""" Дружище, нужно сделать реплай на сообщение со ссылкой""")

    if not re.findall(r'(https?://[^\s]+)', message.reply_to_message.text):
        return message.reply(""" Дружище, нужно сделать реплай на сообщение со ссылкой""")

    url = re.findall(r'(https?://[^\s]+)', message.reply_to_message.text)
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
    )
    qr.add_data(url[0])
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0) 

    await message.reply_photo(photo = BufferedInputFile(file=buf.getvalue(),filename="qr.png"))
