from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, BotCommand
from filters.role import RoleFilter
from models.jaynecobbdatabase import Chats
from bot_utils import deepgetattr, del_command
import re

router = Router()
router.message.filter(F.text)

commands = [
    BotCommand(command='/allow_chat', description="[name] Добавить чат в whitelist"),
    BotCommand(command='/refuse_chat', description="Удалить чат из whitelist"),
]

@router.message(RoleFilter("owner"), Command("allow_chat"))
async def allow_chat(message: Message):
    
    clear_text = del_command(message.text).lower()
    if(not clear_text): 
        await message.answer(text='❔Добавьте команду для чата одним словом')
        return
    if(not validate_text(clear_text)):
        await message.answer(text='❌Не соответствует требованиям (английские буквы, цифры, нижние подчеркивания)')
        return
    
    Chats.get_or_create(
        chat_id=deepgetattr(message, 'chat.id'), 
        chat_title=deepgetattr(message, 'chat.title'),
        link_command_name=clear_text
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
    

def validate_text(text):
    if len(text) > 32:
        return False
    pattern = r'^[a-zA-Z0-9_]+$'
    if re.match(pattern, text):
        return True
    return False

    
