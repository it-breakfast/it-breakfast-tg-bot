from TelegramBot import config
from TelegramBot.logging import LOGGER

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