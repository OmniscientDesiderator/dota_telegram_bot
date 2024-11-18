import os
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from keyboards.player_menu import MyCallback
from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import FSInputFile

from services.dota_api import get_match
from services.current_hero import get_current_hero
from services.match_card import create_match_card

from keyboards.match_menu import MyCallback

router = Router()

class Search(StatesGroup):
    matchId = State()

bans = []
players = []

@router.message(Command('show_match'))
async def show_player(message: Message, state: FSMContext):
    await state.set_state(Search.matchId)
    await message.answer('Пожалуйста введите ID матча.')

@router.message(Search.matchId)
async def search_match(message: Message, state: FSMContext):
    if(message.text.isdigit()):
        await state.update_data(matchId=message.text)
        data = await state.get_data()

        match_data = get_match(data['matchId'])

        for item in match_data['picks_bans']:
            if not item['is_pick']:
                ban = {'hero': item['hero_id'], 'team': item['team']}
                bans.append(ban)

    create_match_card(data['matchId'], match_data)

    image_path = f'../app/images/{data['matchId']}.png'
    if os.path.exists(image_path):
        with open(image_path, 'rb'):
            photo = FSInputFile(image_path)
            await message.answer_photo(photo=photo)
    else:
        await message.answer('Пожалуйста введите ID матча.')
    os.remove(image_path)
            
@router.callback_query(MyCallback.filter(F.foo == 'Баны'))
async def player_heroes(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    match_info = []

    for ban in bans:
        hero = get_current_hero(ban['hero'])
        team = 'света' if ban['team'] == 0 else 'тьмы'
        match_info.append(f'{hero} (Силы {team})')

    match_info_str = '\n\n'.join(match_info)
    await callback.message.answer(f'Баны матча {data['matchId']}\n\n{match_info_str}')
        