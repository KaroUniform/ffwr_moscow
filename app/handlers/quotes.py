from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, BotCommand
from filters.role import RoleFilter
from models.jaynecobbdatabase import Quotes
from bot_utils import deepgetattr, del_command

router = Router()
router.message.filter(F.text)
commands = [
    BotCommand(command='/quote', description="(#) Вывести случайную цитату или номер #"),
    BotCommand(command='/allquotes', description="Вывести список доступных номеров цитат"),
    BotCommand(command='/aquote', description="[reply_to_message] Добавить цитату"),
    BotCommand(command='/rmquote', description="[#] Удалить цитату номер #"),
    BotCommand(command='/addmultiline', description="[text] Произвольный текст в цитату"),
]


@router.message(Command('quote'))
async def quote(message: Message, bot: Bot):
    
    q_number = del_command(message.text)
    if q_number.isdigit(): q_number = int(q_number)
    else: q_number = None
    
    
   
        

@router.message(Command('allquotes'))
async def allquotes(message: Message, bot: Bot):
    pass

@router.message((F.reply_to_message), Command('aquote'), RoleFilter('moderator'))    
@router.message((F.reply_to_message), Command('aquote'), RoleFilter('admin'))
@router.message((F.reply_to_message), Command('aquote'), RoleFilter('owner'))
async def aquote(message: Message, bot: Bot):
    pass
    
@router.message(Command('rmquote'))
async def rmquote(message: Message, bot: Bot):
    pass

@router.message(Command('addmultiline'))
async def addmultiline(message: Message, bot: Bot):
    pass
    