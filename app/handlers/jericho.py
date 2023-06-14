from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, BotCommand
from asyncio import sleep
from filters.role import RoleFilter
from models.jaynecobbdatabase import Chats, UsersToChats
from bot_utils import deepgetattr, del_command

router = Router()
router.message.filter(F.text)
commands = [
    BotCommand(command='/jericho', description="[reply_to_message] заблокировать пользователя во всех чатах"),
]

@router.message((F.reply_to_message), Command('jericho'), RoleFilter('owner'))
async def jericho(message: Message, bot: Bot):
    
    clear_text = del_command(message.text).lower()
    
    if('заблокировать везде' not in clear_text): 
        await message.reply(text=f'❗️Подтверди свое решение словом "заблокировать везде" после команды')
        return
    
    full_name = deepgetattr(message, 'reply_to_message.from_user.full_name')
    chats = Chats.select().execute()
    error_in_chat = []
    
    for chat in chats:
        try:
            await bot.ban_chat_member(
                chat.chat_id, 
                message.reply_to_message.from_user.id
            )
            UsersToChats.update(is_banned=True).where(
                (UsersToChats.user == message.reply_to_message.from_user.id) 
                & (UsersToChats.chat==chat.chat_id)
            ).execute()
            await sleep(0.1)
        except TelegramBadRequest:
            error_in_chat.append(chat.chat_title)
    
    successful = f'🕯 Пользователь {full_name} заблокирован.'   
    unsuccessful = f'\nНеудачно: {", ".join(error_in_chat)}' if len(error_in_chat) > 0 else ""
    await message.reply(text=successful+unsuccessful)
    
    
        

        

        
    
    
