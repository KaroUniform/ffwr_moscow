from typing import Callable, Dict, Any, Awaitable
from models.jaynecobbdatabase import Chats, Users, Roles, UsersToChats
from models.logdb import Log
from bot_utils import deepgetattr

from aiogram import BaseMiddleware, F
from aiogram.types import Message

class WhitelistMessageMiddleware(BaseMiddleware):
    
    #TODO все кеширующиеся значения перенести в settings и доставать оттуда динамично с возможностью обновления
    allowed_chat_cached = set([chat.chat_id for chat in Chats.select(Chats.chat_id)])
    owner_role = Roles.get(Roles.name == 'owner')
    chat_to_log = set([chat.chat_id for chat in Chats.select(Chats) if chat.log_text])
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        
        if (event.chat.id in self.allowed_chat_cached):
            if event.chat.id in self.chat_to_log: self.save_log(event)
            Users.get_or_create(user_id=event.from_user.id)
            UsersToChats.get_or_create(user_id=event.from_user.id, chat_id=event.chat.id)
            return await handler(event, data)
        
        # Доступна оптимизация, ведь владельцы меняются экстремально редко
        if UsersToChats.select().where(
            (UsersToChats.user == event.from_user.id) 
            & (UsersToChats.role == self.owner_role.role_id)
        ).count():
            return await handler(event, data)
     
    #Корректно сохраняется только текст    
    def save_log(self, message: Message):
        Log.create(
            chat_id = deepgetattr(message, 'chat.id'),
            chat_title = deepgetattr(message, 'chat.title'),
            chat_username = deepgetattr(message, 'chat.username'),
            forward_date = deepgetattr(message, 'forward_date'),
            forward_from_chat_id = deepgetattr(message, 'forward_from_chat.id'),
            forward_from_chat_title = deepgetattr(message, 'forward_from_chat.title'),
            forward_from_chat_username = deepgetattr(message, 'forward_from_chat.username'),
            forward_from_user_id = deepgetattr(message, 'forward_from.id'),
            forward_from_user_username = deepgetattr(message, 'forward_from.username'),
            forward_user_first_name = deepgetattr(message, 'forward_from.first_name'),
            from_user_first_name = deepgetattr(message, 'from_user.first_name'),
            from_user_id = deepgetattr(message, 'from_user.id'),
            from_user_is_bot = deepgetattr(message, 'from_user.is_bot'),
            from_user_last_name = deepgetattr(message, 'from_user.last_name'),
            from_user_username = deepgetattr(message, 'from_user.username'),
            message_date = deepgetattr(message, 'date'),
            message_edit_date = deepgetattr(message, 'edit_date'),
            message_id = deepgetattr(message, 'message_id'),
            message_text = deepgetattr(message, 'text'),
            reply_to_message_from_username = deepgetattr(message, 'reply_to_message.from_user.username'),
            reply_to_message_id = deepgetattr(message, 'reply_to_message.message_id'),
            reply_to_message_text = deepgetattr(message, 'reply_to_message.text')
        )
            
