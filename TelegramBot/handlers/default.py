import asyncio
from datetime import datetime

from TelegramBot.keyboards.main import get_menu_kb
from TelegramBot.helpers.cron import message_state, utc_to_local
from TelegramBot.logging import LOGGER

from aiogram import Bot
from aiogram import Router, F
from aiogram.types import (
    Message, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, PreCheckoutQuery,  
)
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BufferedInputFile

from TelegramBot.helpers.admin_filter import IsAdmin, IsPinned
from TelegramBot.config import ADMINS, CHAT_ID
from TelegramBot import bot

import re
import io
import qrcode

default_router = Router()
message_time_router = Router()

@message_time_router.message()
async def save_message_time(message: Message) -> None:
    """
    Сохраняет время последнего сообщения в чате.
    """
    message_state.last_message_time = utc_to_local(message.date)
    LOGGER(__name__).info(f"Сохранено время последнего сообщения: {message_state.last_message_time}")

@default_router.message(CommandStart())
async def default_handler(message: Message) -> None:
    await message.answer('Извините, я не говорю по-русски.', )

@default_router.message(IsAdmin(ADMINS), IsPinned())
async def default_pinned_message(message: Message) -> None:
    pinned_message_id = message.pinned_message.message_id
    await bot.send_message(
        chat_id=message.chat.id,
        text="Hам указали место. Славься великая @bashechka !",
        reply_to_message_id=pinned_message_id
    )

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

@default_router.message(Command('link'))
async def send_link(message: Message):

    if not message.reply_to_message is not None:
        return message.reply(""" Дружище, нужно сделать реплай на сообщение со ссылкой""")

    internal_id = str(message.chat.id)[4:]

    url = f"https://t.me/c/{internal_id}/{message.message_id}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0) 

    await message.reply_photo(photo = BufferedInputFile(file=buf.getvalue(),filename="qr.png"))
