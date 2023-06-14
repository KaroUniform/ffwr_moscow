from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, BotCommand
from filters.role import RoleFilter
from models.jaynecobbdatabase import Chats
from aiogram.filters import Command

router = Router()
router.message.filter(F.text)
commands = [
    BotCommand(command='/voices', description="Вкл/выкл голосовые"),
]


@router.message(Command('voices'), RoleFilter('moderator'))
@router.message(Command('voices'), RoleFilter('admin'))
@router.message(Command('voices'), RoleFilter('owner'))
async def voice(message: Message, bot: Bot):
    
    chat = Chats.get(chat_id=message.chat.id)
    new_permissions = (await bot.get_chat(message.chat.id)).permissions
    new_permissions.can_send_voice_notes = not chat.remove_voices
    try:
        await bot.set_chat_permissions(
            chat_id=message.chat.id,
            use_independent_chat_permissions=True,
            permissions=new_permissions
        )
        await message.reply(text=f'Голосовые сообщения теперь {"🔊разрешены" if not chat.remove_voices else "🔇запрещены"}') 
    
    except TelegramBadRequest:
        await message.reply(
            text=f'😢Не имею доступа к изменению настроек голосовых сообщений, не хватает прав в чате',
        )
    
    chat.remove_voices = not chat.remove_voices
    chat.save()
        