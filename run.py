import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import match_handler, player_handler, start_handler

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_routers(match_handler.router, player_handler.router, start_handler.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
