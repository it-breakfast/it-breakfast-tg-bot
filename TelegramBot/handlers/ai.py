from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from TelegramBot.helpers.userbot import get_last_100_messages
from TelegramBot.helpers.openai import response_openai
from TelegramBot import bot
from TelegramBot import config

ai_router = Router()

prompt = """
Это последние сообщения из чата.
Дай саммари что тут происходит чтобы человек не читающий пару дней чат быстро вошел в контекст происходящего.
Не говори в целом про чат, говори о том что было конкретное в сообщениях
"""

@ai_router.message(Command('last100'))
async def last100(message: Message):
    await bot.send_chat_action(chat_id=config.CHAT_ID, action="typing")
    text = await get_last_100_messages()
    ai_anwser= await response_openai(text, prompt)
    await message.answer(str(ai_anwser))
