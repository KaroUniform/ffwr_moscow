import asyncio
from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.types import Message
from models.jaynecobbdatabase import Chats
from bot_config import config


class LinkersFilter(BaseFilter):
    
    #TODO перенести значения в settings и динамических их оттуда получать
    chats = set(["/"+chat.link_command_name for chat in Chats.select().execute() if chat.link_command_name is not None])
    chats_with_username = set(["/"+chat.link_command_name + config.bot_name for chat in Chats.select().execute() if chat.link_command_name is not None])
        
    
    async def __call__(self, message: Message) -> bool:

        return (message.text in self.chats_with_username) or (message.text in self.chats)
    
