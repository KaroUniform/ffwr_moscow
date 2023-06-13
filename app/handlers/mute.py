import datetime
from aiogram import Router, F, Bot
from aiogram.types import ChatPermissions
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message
from filters.role import RoleFilter
from bot_utils import deepgetattr, del_command

router = Router()
router.message.filter(F.text)
@router.message((F.reply_to_message), Command('mute'), RoleFilter('moderator'))
@router.message((F.reply_to_message), Command('mute'), RoleFilter('admin'))
@router.message((F.reply_to_message), Command('mute'), RoleFilter('owner'))
async def mute(message: Message, bot: Bot):
    
    full_name = deepgetattr(message, 'reply_to_message.from_user.full_name')
    until = del_command(message.text)
    if until.isdigit(): until = int(until)
    else: until = 1
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
        await message.reply(
            text=f'🔇Пользователь {full_name} ограничен до {str(until)[:-7]}',
        )
        
    except TelegramBadRequest:
        await message.reply(
            text=f'😢Не имею доступа к этой команде, не хватает прав в чате',
        )