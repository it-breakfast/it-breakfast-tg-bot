import asyncio

from TelegramBot.handlers import register_handlers

from TelegramBot.logging import LOGGER
from TelegramBot import dp,bot
from TelegramBot import scheduler
from TelegramBot import client_userbot

async def main():

    LOGGER(__name__).info("✅ Бот запущен. Ожидание сообщений и выполнение задачи ..")
    scheduler.start()
    register_handlers(dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
