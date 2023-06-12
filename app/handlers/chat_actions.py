from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import Message
from filters.role import RoleFilter
from models.jaynecobbdatabase import Chats
from bot_utils import deepgetattr

router = Router()
router.message.filter(F.text)

@router.message(RoleFilter("owner"), Command("allow_chat"))
async def allow_chat(message: Message):
    

    Chats.get_or_create(
        chat_id=deepgetattr(message, 'chat.id'), 
        chat_title=deepgetattr(message, 'chat.title')
    )
    
    await message.answer(
        text='✅ Чат добавлен в whitelist',
    )

@router.message(RoleFilter("owner"), Command("refuse_chat"))
async def refuse_chat(message: Message):
    chat = Chats.get(
        chat_id=message.chat.id
    )
    if chat: chat.delete_instance()
    await message.answer(
        text='💥Данные чата уничтожены, чат удален из whitelist',
    )


@router.message(Command("allow_chat"))
@router.message(Command("refuse_chat"))
async def other_chat(message: Message):
    await message.answer(
        text="🛑У Вас нет права на использование этой команды",
    )
    
