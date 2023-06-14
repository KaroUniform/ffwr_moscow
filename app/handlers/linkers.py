from datetime import datetime, timedelta
from aiogram import Router, F, Bot
from aiogram.types import Message, BotCommand
from models.jaynecobbdatabase import Chats
from filters.linkers import LinkersFilter
from aiogram.exceptions import TelegramBadRequest
from aiogram import html

router = Router()
router.message.filter(F.text, LinkersFilter())

commands = [
    BotCommand(
        command="/" + chat.link_command_name, description=f"Ссылка на {chat.chat_title}"
    )
    for chat in [
        chat for chat in Chats.select().execute() if chat.link_command_name is not None
    ]
]

# Доделать динамическое обновление
@router.message()
async def allow_chat(message: Message, bot : Bot):
    chat_nickname = message.text[1:]
    if chat_nickname.find("@") != -1: chat_nickname = chat_nickname[:chat_nickname.find("@")]
    chat = Chats.get(link_command_name=chat_nickname)
    expire_date = datetime.now() + timedelta(minutes=30)
    try:
        link = await bot.create_chat_invite_link(
            chat_id=chat.chat_id,
            expire_date=expire_date,
            member_limit=1
        )
    except TelegramBadRequest:
        await message.reply(f"🙁Не получилось сделать ссылку, нет прав в целевом чате")
        return
    await message.reply(f"🚪Ваша {html.link('ссылка', link.invite_link)} на чат {html.bold(html.quote(chat.chat_title))}", protect_content=True, parse_mode="HTML")
