from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from TelegramBot.helpers.cron import message_state
from TelegramBot.logging import LOGGER
from datetime import timezone

class MessageTimeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Конвертируем naive datetime в aware datetime с UTC
        message_state.last_message_time = event.date.replace(tzinfo=timezone.utc)
        LOGGER(__name__).info(f"Сохранено время последнего сообщения: {message_state.last_message_time}")
        
        # Продолжаем обработку сообщения
        return await handler(event, data) 