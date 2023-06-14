from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, BotCommand
from filters.role import RoleFilter
from models.jaynecobbdatabase import Chats
from bot_utils import deepgetattr, del_command

router = Router()
router.message.filter(F.text)

commands = [
    BotCommand(command='/allow_chat', description="Добавить чат в whitelist"),
    BotCommand(command='/refuse_chat', description="Удалить чат из whitelist"),
]

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
    
    clear_text = del_command(message.text).lower()
    if('уничтожить чат' not in clear_text): 
        await message.reply(text=f'❗️Подтверди свое решение текстом "уничтожить чат" после команды')
        return
    
    chat = Chats.get(
        chat_id=message.chat.id
    )
    if chat: chat.delete_instance()
    await message.answer(
        text='💥Данные чата уничтожены, чат удален из whitelist',
    )

    
