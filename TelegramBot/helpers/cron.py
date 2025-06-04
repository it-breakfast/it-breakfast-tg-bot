from TelegramBot import config
from TelegramBot.logging import LOGGER
from datetime import datetime, timedelta, timezone
import random
import inspect
from .message_generator import generate_message

chat_id=config.CHAT_ID

class MessageState:
    def __init__(self):
        self.last_message_time = None

message_state = MessageState()

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
    LOGGER(__name__).info(f"last_message_time: {message_state.last_message_time}")
    if message_state.last_message_time is None:
        return
        
    current_time = datetime.now(timezone.utc)
    time_diff = current_time - message_state.last_message_time
   
    if time_diff > timedelta(minutes=0):
        try:
            message = await generate_message()
            await bot.send_message(chat_id, message)
            LOGGER(__name__).info("Отправлено сгенерированное сообщение в чат")
        except Exception as e:
            LOGGER(__name__).info(f"Не удалось отправить сообщение: {e}")
   
