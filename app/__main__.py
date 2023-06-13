import asyncio
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from aiogram import Bot, Dispatcher
from bot_config import config
from handlers import echo, chat_actions, base, ban, mute, voice
from middleware.whitelist import WhitelistMessageMiddleware




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
    dp.message.middleware(WhitelistMessageMiddleware())
    dp.include_routers(
        echo.router,
        chat_actions.router,
        ban.router,
        mute.router,
        voice.router,
        base.router # Make shure it's the last handler
    )
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
