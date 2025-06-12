from TelegramBot import config
from TelegramBot.logging import LOGGER
from datetime import datetime, timedelta, timezone, tzinfo
import random
import inspect
from .message_generator import generate_message
from TelegramBot.helpers.admin_filter import IsNight
from TelegramBot.helpers.local_timezone import bangkok_tz
from TelegramBot.helpers.user_limits import reset_limits

chat_id=config.CHAT_ID

class MessageState:
    def __init__(self):
        self.last_message_time = None

message_state = MessageState()

# Список возможных никнеймов для бота
BOT_NICKNAMES = [
    "IT-Завтрак Бот",
    "Я сегодня жесткий",
    "Я сегодня Бот",
    "Жесткий Айтишник",
    "Помощник Завтрака"
]

async def scheduled_job(bot):
    try:
        await bot.send_message(chat_id, "Привет @bashechka ! Время крутить барабан 🗓️")
        LOGGER(__name__).info("Сообщение отправлено")
    except Exception as e:
        LOGGER(__name__).info("Не удалось отправить сообщение: {e}")

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(bangkok_tz)

async def check_last_message(bot):
    """
    Проверяет время последнего сообщения и отправляет уведомление, если прошло более 4 минут.
    """
    LOGGER(__name__).info(f"last_message_time: {message_state.last_message_time}")
    if message_state.last_message_time is None:
        return

    current_time = datetime.now(bangkok_tz)
    time_diff = current_time - message_state.last_message_time
    
    IsNight(current_time)

    if time_diff > timedelta(hours=6) and not IsNight(current_time):
        try:
            message = await generate_message()
            await bot.send_message(chat_id, message)
            LOGGER(__name__).info("Отправлено сгенерированное сообщение в чат")
            message_state.last_message_time = current_time
        except Exception as e:
            LOGGER(__name__).info(f"Не удалось отправить сообщение: {e}")
    else:
        LOGGER(__name__).info(f"time_diff сейчас {time_diff} что меньше {timedelta(hours=6)}")
        LOGGER(__name__).info(f"IsNight {IsNight(current_time)}")
   

async def reset_limits_job():
    """
    Сбрасывает лимиты пользователей по расписанию.
    """
    reset_limits()
    LOGGER(__name__).info("Лимиты пользователей сброшены")
   

async def change_bot_nickname(bot):
    """
    Меняет никнейм бота на случайный из списка.
    """
    try:
        new_nickname = random.choice(BOT_NICKNAMES)
        await bot.set_my_name(new_nickname)
        LOGGER(__name__).info(f"Никнейм бота успешно изменен на: {new_nickname}")
    except Exception as e:
        LOGGER(__name__).info(f"Не удалось изменить никнейм бота: {e}")
   
