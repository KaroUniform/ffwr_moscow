from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, BotCommand
from filters.role import RoleFilter
from models.jaynecobbdatabase import Quotes
from bot_utils import deepgetattr, del_command
import random
from aiogram import html
from peewee import fn

router = Router()
router.message.filter(F.text)
commands = [
    BotCommand(command='/quote', description="(#) Вывести случайную цитату или номер #"),
    BotCommand(command='/allquotes', description="Вывести список доступных номеров цитат"),
    BotCommand(command='/aquote', description="[reply_to_message] Добавить цитату"),
    BotCommand(command='/rmquote', description="[#] Удалить цитату номер #"),
    BotCommand(command='/addmultiline', description="[text] Произвольный текст в цитату"),
    BotCommand(command='/horoscope', description="Гадание по цитатам"),
]

spells = [
    "ахалай-махалай",
    "ляськи-масяськи",
    "сим-салабим",
    "пикапу-трикапу",
    "лорики-ёрики",
    "снип-снап-снурре",
    "снурре-базилюрре",
    "бофара-чуфара",
    "абра-кадабра",
    "трах-тибидох",
    "колдуй бабка, колдуй дед",
    "флюггегехаймен",
    "скорики-морики",
    "крибле-крабле-бумс",
    "крекс-пекс-фекс",
    "керальтус-нивус",
    "бип-боп",
    "бип-буп"
]

@router.message(Command('horoscope'))
async def horoscope(message: Message):
    global spells
    q = Quotes.select(Quotes.text).order_by(fn.Random()).limit(1)
    italic = html.italic(f"{random.choice(spells).capitalize()}, {random.choice(spells)}! Вот что судьба тебе готовит!")
    await message.reply(
        f"{italic}\n\n {html.code(html.quote(q.get().text))}", 
        parse_mode='HTML'
    )
    
@router.message(Command('quote'))
async def quote(message: Message):
    
    q_number = del_command(message.text)
    if q_number.isdigit(): 
        q = Quotes.get_or_none(quote_id=int(q_number))
        if q: 
            author = f"{html.bold(q.author_username)}:\n " if q.author_username != "multiline" else ""
            by = html.italic("#"+str(q.quote_id)+ " submitted by "+ q.submitter_name + " at " + q.create_time.strftime('%Y-%m-%d'))
            await message.reply(f"{author}{html.code(html.quote(q.text))}\n\n {by}", parse_mode='HTML')
            return
            
    q_list = [quote for quote in Quotes.select().execute()]
    if(not q_list):
        await message.reply("Нет сохраненных цитат")
        return
        
    q = random.choice(q_list)
    author = f"{html.bold(q.author_username)}:\n " if q.author_username != "multiline" else ""
    by = html.italic(
        "#"+str(q.quote_id)
        +" submitted by "
        +q.submitter_name 
        +" at "
        +q.create_time.strftime('%Y-%m-%d')
    )
    
    await message.reply(
        f"{author}{html.code(html.quote(q.text))}\n\n {by}", parse_mode='HTML'
    )
    

@router.message(Command('allquotes'))
async def allquotes(message: Message):
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

@router.message(Command('rmquote'), RoleFilter('moderator'))    
@router.message(Command('rmquote'), RoleFilter('admin'))
@router.message(Command('rmquote'), RoleFilter('owner'))
async def rmquote(message: Message,):
    number = del_command(message.text)
    if not number.isdigit(): 
        await message.reply(f'#️⃣Для удаления цитаты необходимо указать действительный номер')
        return
    number = int(number)
    q =  Quotes.get_or_none(quote_id=number)
    if not q:
        await message.reply(f'❓Такой цитаты не существует')
        return
    q.delete_instance()
    await message.reply(f'Цитата {number} удалена')


@router.message(Command('addmultiline'), RoleFilter('owner'))
async def addmultiline(message: Message):
    multiline_q = del_command(message.text)
    if(not multiline_q):
        await message.reply(f'Вставьте любое сообщение после команды для сохранения в цитаты')
        return

    new_q = Quotes.create(
        chat=message.chat.id,
        submitter=message.from_user.id,
        submitter_name=message.from_user.username,
        text=multiline_q.strip("\n"),
        author_username="multiline"
    )
    await message.reply(f'Цитата сохранена под номером '+ str(new_q.quote_id))
    