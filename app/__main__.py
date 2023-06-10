import asyncio
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from bot_config import config
from handlers import echo



async def main() -> None:
    path = os.path.abspath(os.path.dirname(__file__))
    os.makedirs(path+'/log/', exist_ok=True)
    time_rotating_handler = TimedRotatingFileHandler(
        path+'/log/Cobb.log', 
        when="midnight", 
        interval=7, 
        backupCount=60
    )
    logging.basicConfig(
        format="[%(asctime)s][%(levelname)s] %(message)s",
        level=logging.INFO,
        handlers=[
            time_rotating_handler, 
            logging.StreamHandler()
        ],
        datefmt="%d.%m.%Y %H:%M:%S",
    )
    bot = Bot(
        token=config.bot_token.get_secret_value()
    )
    dp = Dispatcher()
    dp.include_routers(echo.router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
