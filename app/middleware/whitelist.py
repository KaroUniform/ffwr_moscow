from typing import Callable, Dict, Any, Awaitable
from models.jaynecobbdatabase import Chats, Users, Roles

from aiogram import BaseMiddleware
from aiogram.types import Message

class WhitelistMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        allowed_chats = list(Chats.select(Chats.chat_id))

        user = Users.get(Users.user_id == event.from_user.id)
        
        admin_role = Roles.get(Roles.name == 'admin')
        if (event.chat.id in allowed_chats) or (user.role_id >= admin_role.role_id):
            return await handler(event, data)
            
