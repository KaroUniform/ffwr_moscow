import datetime
from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import ChatPermissions
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, BotCommand
from filters.role import RoleFilter
from models.jaynecobbdatabase import UsersToChats
from bot_utils import deepgetattr

router = Router()
router.message.filter(F.text)

commands = [
    BotCommand(command='/warn', description="[reply_to_message] добавить предупреждение"),
    BotCommand(command='/unwarn', description="[reply_to_message] снять предупреждение"),
]

@router.message((F.reply_to_message), Command('warn'), RoleFilter('moderator'))
@router.message((F.reply_to_message), Command('warn'), RoleFilter('admin'))
@router.message((F.reply_to_message), Command('warn'), RoleFilter('owner'))
async def warn(message: Message, bot: Bot):
    
    full_name = deepgetattr(message, 'reply_to_message.from_user.full_name')
    user_in_chat, created = UsersToChats.get_or_create(
        chat=message.chat.id,
        user=message.reply_to_message.from_user.id
    )

    if user_in_chat.warn_count < 2:
        user_in_chat.warn_count += 1
        await message.reply(
            text=f'⚠️{full_name} получил предупреждение, теперь их {user_in_chat.warn_count}',
        )
        user_in_chat.save()
        return
    
    if (user_in_chat.warn_count >= 2) and (user_in_chat.warn_count <4):
        until = 24
        until = datetime.datetime.now() + datetime.timedelta(hours=until)
        try:
            await bot.restrict_chat_member(
                message.chat.id, 
                message.reply_to_message.from_user.id,
                permissions=ChatPermissions(
                    can_send_messages= False,
                    can_send_audios= False,
                    can_send_documents= False,
                    can_send_photos= False,
                    can_send_videos= False,
                    can_send_video_notes= False,
                    can_send_voice_notes= False,
                    can_send_polls= False,
                    can_send_other_messages= False,
                    can_add_web_page_previews= False,
                    can_change_info= False,
                    can_invite_users= False,
                    can_pin_messages= False,
                    can_manage_topics= False
                ),
                until_date=until
            )
            user_in_chat.warn_count += 1
            user_in_chat.is_banned = True
            user_in_chat.save()
            await message.reply(
                text=f'🔇Пользователь {full_name} ограничен до {str(until)[:-7]} из-за большого количества предупреждений: {user_in_chat.warn_count}',
            )
        
        except TelegramBadRequest:
            await message.reply(
                text=f'😢Не имею доступа к этой команде, не хватает прав в чате',
            )
        return
    
    
    try:
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
async def warn(message: Message, bot: Bot):
    
    full_name = deepgetattr(message, 'reply_to_message.from_user.full_name')
    user_in_chat, created = UsersToChats.get_or_create(
        chat=message.chat.id,
        user=message.reply_to_message.from_user.id
    )
    
    if user_in_chat.warn_count == 0:
        await message.reply(
            text=f'🛑{full_name} не имеет действующих предупреждений: {user_in_chat.warn_count}',
        )
        return
    
    if user_in_chat.warn_count != 5:
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
            message.reply_to_message.from_user.id,
            only_if_banned=True,
        )
        user_in_chat.is_banned = False
        user_in_chat.save()
    except TelegramBadRequest:
        await message.reply(
            text=f'😢Не имею доступа к этой команде, не хватает прав в чате',
        )
        

        
    
    
