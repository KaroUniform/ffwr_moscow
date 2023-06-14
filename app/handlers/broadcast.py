from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, BotCommand
from asyncio import sleep
from filters.role import RoleFilter
from models.jaynecobbdatabase import Chats

router = Router()
router.message.filter(F.text)

commands = [
    BotCommand(command='/broadcast', description="[reply_to_message] Переслать сообщение во все чаты"),
]

@router.message((F.reply_to_message), Command('broadcast'), RoleFilter('owner'))
async def broadcast(message: Message, bot: Bot):
    await bot.get_my_commands()
    
    chats = Chats.select().execute()
    error_in_chat = []
    
    for chat in chats:
        try:
            await bot.forward_message(chat.chat_id, message.chat.id, message.reply_to_message.message_id)
            await sleep(0.1)
        except TelegramBadRequest:
            error_in_chat.append(chat.chat_title)
    
    successful = f'📨Сообщение отправлено.\nудачно: {len(chats) - len(error_in_chat)};'    
    unsuccessful = f'\nНеудачно: {", ".join(error_in_chat)}' if len(error_in_chat) > 0 else ''
    await message.reply(text=successful+unsuccessful)
    
    
        

        

        
    
    
