from aiogram import Router, F
from aiogram.types import Message


router = Router()

@router.message()
async def cmd_start(message: Message):
    return
    # await message.reply_sticker('CAACAgIAAx0CaJZtbgACEqVkh3SMPMgap7qMSc33DGHhTuUZ3AACXCgAAlpvGUgMxewk-BAF-i8E')