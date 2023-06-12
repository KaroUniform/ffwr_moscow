from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import Message
from filters.role import RoleFilter

router = Router()

@router.message(RoleFilter('owner') or RoleFilter('admin'), Command("echo"))
async def cmd_start(message: Message):
    await message.answer(
        text=str(message),
    )