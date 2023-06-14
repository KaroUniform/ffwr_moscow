from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message
from asyncio import sleep
from filters.role import RoleFilter
from models.jaynecobbdatabase import Chats, UsersToChats
from bot_utils import deepgetattr, del_command

router = Router()
router.message.filter(F.text)


@router.message((F.reply_to_message), Command('jericho'), RoleFilter('owner'))
async def jericho(message: Message, bot: Bot):
    
    clear_text = del_command(message.text)
    
    if('yes' not in clear_text): 
        await message.reply(text=f'👀Подтверди свое решение словом "yes" после команды')
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
        
    await message.reply(text=f'🕯 Пользователь {full_name} заблокирован.\nудачно: {len(chats) - len(error_in_chat)};\nНеудачно: {", ".join(error_in_chat)}',)
    
    
        

        

        
    
    
