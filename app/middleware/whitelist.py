from typing import Callable, Dict, Any, Awaitable
from models.jaynecobbdatabase import Chats, Users, Roles, UsersToChats

from aiogram import BaseMiddleware
from aiogram.types import Message

class WhitelistMessageMiddleware(BaseMiddleware):
    
    allowed_chat_cached = [chat.chat_id for chat in Chats.select(Chats.chat_id)]
    owner_role = Roles.get(Roles.name == 'owner')
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        
        
        is_owner = UsersToChats.select().where(
            (UsersToChats.user == event.from_user.id) & (UsersToChats.role == self.owner_role.role_id)
        ).count()
        
        if (event.chat.id in self.allowed_chat_cached) or is_owner:
            return await handler(event, data)
            
