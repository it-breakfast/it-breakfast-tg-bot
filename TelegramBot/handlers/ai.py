from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from TelegramBot.helpers.userbot import get_last_100_messages
from TelegramBot.helpers.openai import response_openai, response_openai_image
from TelegramBot.helpers.google_search import google_search
from TelegramBot import bot
from TelegramBot import config
from TelegramBot.helpers.user_limits import get_and_increment_limit

from aiogram.types import BufferedInputFile
import io

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
Ты чат-бот помощник чата "IT-завтрак Пхукет".
Отвечай на русском языке.
Ответ должен занимать строго не более не более 600 символов.
"""

prompt_hey_bot_search = """
Ты чат-бот помощник чата "IT-завтрак Пхукет".
Отвечай на русском языке.
Ответ должен занимать строго не более не более 600 символов.

Вот результаты поиска и анализа по твоему запросу:
{search_results}

Проанализируй эту информацию и:
1. Если найдены контактные данные (email, телефоны), сообщи об этом
2. Если найдена личная информация, которая может помочь идентифицировать человека, сообщи об этом
3. Сделай выводы на основе найденной информации
4. Будь осторожен с личной информацией и не раскрывай её полностью

Используй эту информацию для формирования более точного ответа.
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

@ai_router.message(F.text.lower().contains("эй бот"), F.text.lower().contains("нарисуй"))
async def hey_bot_image(message: Message):
    chat_id = message.chat.id
    async with typing(chat_id):
        img = await response_openai_image(message.text)

    await message.reply_photo(photo = BufferedInputFile(file=img, filename="a.png"))

@ai_router.message(F.text.lower().contains("эй бот"))
async def hey_bot(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    count = get_and_increment_limit(user_id)
    
    if count == 2:
        await message.answer("Пожалуйста, пообщайся с реальными людьми.")
        return
    if count == 3:
        await message.answer("Еще раз сегодня напишешь \"эй бот\", и я запишу тебя в список онанистов.")
        return
    if count == 4:
        await message.answer(f"@{message.from_user.username} записан в список онанистов")
        return
    if count > 4:
        return
        
    async with typing(chat_id):
        ai_answer = await response_openai("gpt-4.1-mini", message.text, prompt_hey_bot)
    await message.answer(str(ai_answer))

@ai_router.message(F.text.lower().contains("эй бот"), F.text.lower().contains("найди"))
async def hey_bot_search(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    count = get_and_increment_limit(user_id)
    
    if count == 2:
        await message.answer("Пожалуйста, пообщайся с реальными людьми.")
        return
    if count == 3:
        await message.answer("Еще раз сегодня напишешь \"эй бот\", и я запишу тебя в список онанистов.")
        return
    if count == 4:
        await message.answer(f"@{message.from_user.username} записан в список онанистов")
        return
    if count > 4:
        return
        
    async with typing(chat_id):
        # Получаем результаты поиска
        search_results = await google_search(message.text)
        
        # Форматируем результаты для промпта
        formatted_results = []
        for result in search_results:
            if 'error' in result:
                continue
                
            result_text = f"URL: {result['url']}\n"
            result_text += f"Заголовок: {result['title']}\n"
            result_text += f"Описание: {result['description']}\n"
            
            if result['emails']:
                result_text += f"Найденные email: {', '.join(result['emails'])}\n"
            if result['phones']:
                result_text += f"Найденные телефоны: {', '.join(result['phones'])}\n"
                
            formatted_results.append(result_text)
        
        search_results_text = "\n\n".join(formatted_results)
        
        # Формируем промпт с результатами поиска
        current_prompt = prompt_hey_bot_search.format(search_results=search_results_text)
        
        ai_answer = await response_openai("gpt-4.1-mini", message.text, current_prompt)
    await message.answer(str(ai_answer))

