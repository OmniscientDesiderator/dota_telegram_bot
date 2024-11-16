from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Телеграм бот - информационная платформа по Dota 2 с <a href="https://github.com/intoxicated7">открытым исходным кодом</a>\nНапишите /help чтобы познакомиться с нашими командами\n\nАвтор: @vecherinkanulevix', 
                        parse_mode="HTML",
                        disable_web_page_preview=True)
    
@router.message(Command('help'))
async def show_player(message: Message, state: FSMContext):
    await message.answer('Существующие команды:\n\n/show_player - отображение игрока по Steam ID (информация об аккаунте, последние матчи, герои)\n/show_match - отображение матча по номеру')

@router.message(Command('stick'))
async def show_player(message: Message, state: FSMContext):
    # sticker_id = '5314670335402993551'
    # await message.answer_sticker(sticker=sticker_id)
    await message.answer('Текст проверка', parse_mode="HTML")

    #  <custom-emoji-element class="custom-emoji media-sticker-wrapper" data-doc-id="5307962876386885388" data-sticker-emoji="👰‍♀️"></custom-emoji-element>