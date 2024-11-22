import os
import logging
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import FSInputFile
from aiogram.types import Message

from services.dota_api import get_player_info, get_recent_matches, get_player_heroes
from utils.helpers import extract_steam_id
from services.player_card import create_player_card

logging.basicConfig(level=logging.INFO)

class Search(StatesGroup):
    playerId = State()
    matchId = State()

router = Router()

@router.message(Command('show_player'))
async def show_player(message: Message, state: FSMContext):
    await state.set_state(Search.playerId)
    await message.answer('Отправьте пожалуйста ссылку на Steam пользователя')

@router.message(Search.playerId)
async def search_player(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else 'Без имени'

    logging.info(f'ID: {user_id}, Username: {username}, Message: {message.text}')

    await state.update_data(playerId=message.text)
    data = await state.get_data()

    print(data['playerId'])

    steam_id = extract_steam_id(data['playerId'])
    id_int32 = int(steam_id) % (2**32)

    await state.update_data(playerId=id_int32)

    player_data = get_player_info(id_int32)
    create_player_card(id_int32, player_data)

    image_path = f'../app/images/{id_int32}.png'
    if os.path.exists(image_path):
        with open(image_path, 'rb'):
            photo = FSInputFile(image_path)
            await message.answer_photo(photo=photo)
    else:
        await message.answer('Пожалуйста введите ID матча.')
    os.remove(image_path)
