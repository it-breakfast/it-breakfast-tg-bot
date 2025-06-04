from TelegramBot import config
from TelegramBot.logging import LOGGER
from datetime import datetime, timedelta
import random
import inspect
from .deepseek import generate_message

chat_id=config.CHAT_ID
last_message_time = None  # Глобальная переменная для хранения времени последнего сообщения

async def scheduled_job(bot):
    """
    Задание для планировщика: раз в 2 минуты шлём 'AAAA' в канал.
    """
    try:
        await bot.send_message(chat_id, "Привет @bashechka ! Время крутить барабан 🗓️")
        LOGGER(__name__).info("Сообщение отправлено")
    except Exception as e:
        LOGGER(__name__).info("Не удалось отправить сообщение: {e}")

async def check_last_message(bot):
    """
    Проверяет время последнего сообщения и отправляет уведомление, если прошло более 4 минут.
    """
    global last_message_time
    
    if last_message_time is None:
        return
        
    current_time = datetime.now()
    time_diff = current_time - last_message_time
    await bot.send_message(chat_id, f"last_message_time: {last_message_time}")
    await bot.send_message(chat_id, f"current_time: {current_time}")
    await bot.send_message(chat_id, f"time_diff: {time_diff}")
   
    if time_diff > timedelta(minutes=4):
        try:
            message = await generate_message()
            await bot.send_message(chat_id, message)
            LOGGER(__name__).info("Отправлено сгенерированное сообщение в чат")
        except Exception as e:
            LOGGER(__name__).info(f"Не удалось отправить сообщение: {e}")
   
