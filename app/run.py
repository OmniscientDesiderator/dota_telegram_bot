import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from handlers import match_handler, player_handler, start_handler

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

async def main():
    dp.include_routers(match_handler.router, player_handler.router, start_handler.router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
