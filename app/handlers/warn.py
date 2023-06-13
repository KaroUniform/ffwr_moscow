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

@router.message((F.reply_to_message), Command('warn'), RoleFilter('moderator'))
@router.message((F.reply_to_message), Command('warn'), RoleFilter('admin'))
@router.message((F.reply_to_message), Command('warn'), RoleFilter('owner'))
async def ban(message: Message, bot: Bot):
    
    full_name = deepgetattr(message, 'reply_to_message.from_user.full_name')
    user_in_chat = UsersToChats.get(
        chat=message.chat.id,
        user=message.reply_to_message.from_user.id
    )
    
    if user_in_chat.warn_count < 3:
        user_in_chat.warn_count += 1
        await message.reply(
            text=f'⚠️{full_name} получил предупреждение, теперь их {user_in_chat.warn_count}',
        )
        user_in_chat.save()
        return
    
    try:
        user_in_chat.warn_count += 1
        await bot.ban_chat_member(
            message.chat.id, 
            message.reply_to_message.from_user.id
        )
        await message.reply(
            text=f'🔨{full_name} получил слишком много предупреждений и был заблокирован',
        )
        user_in_chat.warn_count += 1
        user_in_chat.is_banned = True
        user_in_chat.save()
        
    except TelegramBadRequest:
        await message.reply(
            text=f'😢Не имею доступа к этой команде, не хватает прав в чате',
        )
        
@router.message((F.reply_to_message), Command('unwarn'), RoleFilter('moderator'))
@router.message((F.reply_to_message), Command('unwarn'), RoleFilter('admin'))
@router.message((F.reply_to_message), Command('unwarn'), RoleFilter('owner'))
async def unban(message: Message, bot: Bot):
    
    full_name = deepgetattr(message, 'reply_to_message.from_user.full_name')
    user_in_chat = UsersToChats.get(
        chat=message.chat.id,
        user=message.reply_to_message.from_user.id
    )
    
    if user_in_chat.warn_count == 0:
        await message.reply(
            text=f'🛑{full_name} не имеет действующих предупреждений: {user_in_chat.warn_count}',
        )
        return
    
    if user_in_chat.warn_count != 3:
        user_in_chat.warn_count -= 1
        await message.reply(
            text=f'⬇️{full_name} избавлен от предупреждения: {user_in_chat.warn_count}',
        )
        user_in_chat.save()
        return
        
    try:
        user_in_chat.warn_count -= 1
        await message.reply(
            text=f'🔓{full_name} избавлен от предупреждения и был разблокирован: {user_in_chat.warn_count}',
        )
        await bot.unban_chat_member(
            message.chat.id, 
            message.reply_to_message.from_user.id
        )
        user_in_chat.is_banned = False
        user_in_chat.save()
    except TelegramBadRequest:
        await message.reply(
            text=f'😢Не имею доступа к этой команде, не хватает прав в чате',
        )
        

        
    
    
