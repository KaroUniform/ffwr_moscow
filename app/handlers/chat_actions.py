from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import Message

router = Router()

@router.message(Command("allow_chat"))
async def cmd_start(message: Message):
    await message.answer(
        text=str(message),
    )