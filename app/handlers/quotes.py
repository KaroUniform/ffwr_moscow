from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, BotCommand
from filters.role import RoleFilter
from models.jaynecobbdatabase import Quotes
from bot_utils import deepgetattr, del_command
import random
from aiogram import html

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
    if q_number.isdigit(): 
        q = Quotes.get_or_none(quote_id=int(q_number))
        if q: 
            by = html.italic("#"+str(q.quote_id)+ " submitted by "+ q.submitter_name + " at " + q.create_time.strftime('%Y-%m-%d'))
            await message.reply(f"{html.bold(q.author_username)}:\n {html.code(html.quote(q.text))}\n\n {by}", parse_mode='HTML')
            return
            
    q_list = [quote for quote in Quotes.select().execute()]
    if(not q_list):
        await message.reply("Нет сохраненных цитат")
        return
        
    q = random.choice(q_list)
    by = html.italic(
        "#"+str(q.quote_id)
        +" submitted by "
        +q.submitter_name 
        +" at "
        +q.create_time.strftime('%Y-%m-%d')
    )
    await message.reply(
        f"{html.bold(q.author_username)}:\n {html.code(html.quote(q.text))}\n\n {by}", parse_mode='HTML'
    )
    

@router.message(Command('allquotes'))
async def allquotes(message: Message, bot: Bot):
    q_list = [str(q.quote_id) for q in Quotes.select(Quotes.quote_id).execute()]
    q_str = ", ".join([str(q.quote_id) for q in Quotes.select(Quotes.quote_id).execute()])
    await message.reply(f"💬Всего цитат: {len(q_list)}\nСписок доступных номеров цитат: {q_str}")

@router.message((F.reply_to_message), Command('aquote'), RoleFilter('moderator'))    
@router.message((F.reply_to_message), Command('aquote'), RoleFilter('admin'))
@router.message((F.reply_to_message), Command('aquote'), RoleFilter('owner'))
async def aquote(message: Message, bot: Bot):
    
    text = deepgetattr(message, 'reply_to_message.text')
    if(not text):
        text = "https://t.me/c/"+str(abs(message.chat.id))[3:]+"/"+str(message.reply_to_message.message_id)
    
    quote, created = Quotes.get_or_create(
        submitter_name=message.from_user.username,
        submitter=message.from_user.id,
        chat_id=message.chat.id,
        text=text,
        author_username=message.reply_to_message.from_user.username
    )
    await message.reply(f'Цитата была сохранена под номером {quote.quote_id}')

@router.message((F.reply_to_message), Command('rmquote'), RoleFilter('moderator'))    
@router.message((F.reply_to_message), Command('rmquote'), RoleFilter('admin'))
@router.message((F.reply_to_message), Command('rmquote'), RoleFilter('owner'))
async def rmquote(message: Message, bot: Bot):
    number = del_command(message.text)
    if not number.isdigit(): 
        await message.reply(f'Для удаления цитаты необходимо указать действительный номер')
        return
    number = int(number)
    if not Quotes.get_or_none(quote_id=number):
        await message.reply(f'Такой цитаты не существует')
        return

    
        

@router.message(Command('addmultiline'))
async def addmultiline(message: Message, bot: Bot):
    pass
    