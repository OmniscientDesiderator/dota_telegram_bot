from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Телеграм бот - информационная платформа по Dota 2 с <a href="https://github.com/OmniscientDesiderator/dota_telegram_bot">открытым исходным кодом</a>\nНапишите /help чтобы познакомиться с нашими командами\n\nАвтор: @OmniscientDesiderator', 
                        parse_mode="HTML",
                        disable_web_page_preview=True)
    
@router.message(Command('help'))
async def show_player(message: Message):
    await message.answer('Существующие команды:\n\n/show_player - отображение игрока по ссылке Steam (информация об аккаунте, последние матчи, герои)\n/show_match - отображение матча по номеру')