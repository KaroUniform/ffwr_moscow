from aiogram.filters import BaseFilter
from aiogram.types import Message
from models.jaynecobbdatabase import Chats
from bot_config import config

#Несмотря на то, что метод выглядит странно, он работает в 1.5 раза быстрее .startwith и чуть быстрее [0] == '/'
class NotCommandFilter(BaseFilter):
    
    slash = set(['/'])
    
    async def __call__(self, message: Message) -> bool:
        return message.text[0] not in self.slash
    
