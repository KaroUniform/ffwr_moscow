from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import Message
from filters.role import RoleFilter
from models.jaynecobbdatabase import UsersToChats
from bot_utils import deepgetattr

router = Router()
router.message.filter(F.text)


@router.message((F.reply_to_message), Command('ban'), RoleFilter('admin'))
@router.message((F.reply_to_message), Command('ban'), RoleFilter('owner'))
async def ban(message: Message, bot: Bot):
    
    first_name = deepgetattr(message, 'reply_to_message.from_user.first_name') or ""
    last_name = deepgetattr(message, 'reply_to_message.from_user.last_name') or ""
    
    
    try:
        await bot.ban_chat_member(
            message.chat.id, 
            message.reply_to_message.from_user.id
        )
        await message.reply(
            text=f'🔨Пользователь {first_name}{" "+last_name if last_name else ""} заблокирован',
        )
        UsersToChats.update(is_banned=True).where(
            (UsersToChats.user == message.reply_to_message.from_user.id) 
            & (UsersToChats.chat==message.chat.id)
        ).execute()
        
    except TelegramBadRequest:
        await message.reply(
            text=f'😢Не имею доступа к этой команде, не хватает прав в чате',
        )
        

@router.message((F.reply_to_message), Command('unban'), RoleFilter('admin'))
@router.message((F.reply_to_message), Command('unban'), RoleFilter('owner'))
async def unban(message: Message, bot: Bot):
    
    first_name = deepgetattr(message, 'reply_to_message.from_user.first_name') or ""
    last_name = deepgetattr(message, 'reply_to_message.from_user.last_name') or ""
    
    try:
        await bot.unban_chat_member(
            message.chat.id, 
            message.reply_to_message.from_user.id
        )
        await message.reply(
            text=f'❤️Пользователь {first_name}{" "+last_name if last_name else ""} разблокирован',
        )
        UsersToChats.update(is_banned=False).where(
            (UsersToChats.user == message.reply_to_message.from_user.id) 
            & (UsersToChats.chat==message.chat.id)
        ).execute()
        
    except TelegramBadRequest:
        await message.reply(
            text=f'😢Не имею доступа к этой команде, не хватает прав в чате',
        )
        

        
    
    
