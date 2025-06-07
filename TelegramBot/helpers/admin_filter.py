from aiogram.filters import BaseFilter
from aiogram.types import Message
from TelegramBot.helpers.local_timezone import bangkok_tz
import datetime

class IsAdmin(BaseFilter):
    def __init__(self, admin_ids) -> None:
        self.admin_ids = admin_ids
    
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids

class IsPinned(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.pinned_message is not None

def IsNight(x: datetime):
    start = datetime.time(21, 0, 0)
    end = datetime.time(11, 0, 0)
    if start <= end:
        return start <= x.time() <= end
    else:
        return start <= x.time() or x.time() <= end

    