from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsAdmin(BaseFilter):
    def __init__(self, admin_ids) -> None:
        self.admin_ids = admin_ids
    
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids

class IsPinned(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.pinned_message is not None
