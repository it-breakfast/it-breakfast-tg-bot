from TelegramBot import config
from TelegramBot.logging import LOGGER
from datetime import datetime, timedelta
import random
import inspect

chat_id=config.CHAT_ID

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
    Проверяет время последнего сообщения в чате.
    Если прошло больше 6 часов, отправляет напоминание.
    """
    try:
        # Пробуем получить информацию о чате
        try:
            chat = await bot.get_chat(chat_id)
            usernames = await chat.active_usernames
            await bot.send_message(chat_id, f"Активные юзернеймы чата: {usernames}")
        except Exception as e:
            await bot.send_message(chat_id, f"Ошибка при получении информации о чате: {e}")


        # Продолжаем с основной логикой
        async for message in bot.get_chat_history(chat_id, limit=1):
            last_message = message
            break
        else:
            return

        last_message_time = last_message.date
        
        # Проверяем, прошло ли 6 часов
        if datetime.now(last_message_time.tzinfo) - last_message_time > timedelta(minutes=4):
            try:
                # Получаем список администраторов чата
                admins = await bot.get_chat_administrators(chat_id)
                if admins:
                    # Выбираем случайного администратора
                    random_admin = random.choice(admins)
                    username = random_admin.user.username
                    if username:
                        await bot.send_message(chat_id, f"Привет! В чате затишье — не порядок. @{username}, что нового у тебя?")
                    else:
                        await bot.send_message(chat_id, "Привет! В чате затишье — не порядок. Давайте пообщаемся!")
                else:
                    await bot.send_message(chat_id, "Привет! В чате затишье — не порядок. Давайте пообщаемся!")
                await bot.send_message(chat_id, "Отправлено напоминание о неактивности")
            except Exception as e:
                # await bot.send_message(chat_id, f"Ошибка при получении администраторов чата: {e}")
                # await bot.send_message(chat_id, "Привет! В чате затишье — не порядок. Давайте пообщаемся!")
                pass
    except Exception as e:
        # await bot.send_message(chat_id, f"Ошибка при проверке последнего сообщения: {e}")
        LOGGER(__name__).error(f"Ошибка при проверке последнего сообщения: {e}")