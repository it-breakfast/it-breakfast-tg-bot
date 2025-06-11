from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from TelegramBot.helpers.userbot import get_last_100_messages
from TelegramBot.helpers.openai import response_openai
from TelegramBot import bot
from TelegramBot import config

import contextlib
import asyncio
from aiogram.enums import ChatAction

ai_router = Router()

prompt = """
Это последние сообщения из чата.
Дай саммари что тут происходит чтобы человек не читающий пару дней чат быстро вошел в контекст происходящего.
Не говори в целом про чат, говори о том что было конкретное в сообщениях
"""

prompt_hey_bot = """
Отвечай на русском языке.
Ответ должен занимать строго не более не более 600 символов.
"""


async def _typing_loop(chat_id: int):
    try:
        while True:
            await bot.send_chat_action(chat_id=chat_id,
                                       action=ChatAction.TYPING)
            await asyncio.sleep(5)
    except asyncio.CancelledError:
        # Цикл принудительно остановлен – игнорируем исключение.
        pass

@contextlib.asynccontextmanager
async def typing(chat_id: int):
    task = asyncio.create_task(_typing_loop(chat_id))
    try:
        yield                           # даём выполнить «основную» работу
    finally:
        task.cancel()                   # выключаем «typing»
        with contextlib.suppress(asyncio.CancelledError):
            await task


@ai_router.message(Command('last100'))
async def last100(message: Message):
    chat_id = message.chat.id
    async with typing(chat_id):
        text = await get_last_100_messages()
        ai_answer = await response_openai("gpt-4.1", text, prompt)
    await message.answer(str(ai_answer))

@ai_router.message(F.text.lower().contains == "эй бот")
async def hey_bot(message: Message):
    chat_id = message.chat.id
    async with typing(chat_id):
        ai_answer = await response_openai("gpt-4.1-mini", message.text, prompt_hey_bot)
    await message.answer(str(ai_answer))
