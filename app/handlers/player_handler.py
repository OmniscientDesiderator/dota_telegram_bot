from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
import logging
import re
import requests
from config import STEAM_TOKEN

from keyboards.player_menu import MyCallback
import keyboards.player_menu as kb

from services.dota_api import get_player_info, get_recent_matches, get_win_lose, get_player_heroes
from services.ranks import get_player_rank
from services.is_win import get_is_win
from services.current_hero import get_current_hero
from services.get_steam_id import extract_steam_id

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
    win_lose = get_win_lose(id_int32)

    count_matches = win_lose['win'] + win_lose['lose']
    winrate = round((win_lose['win'] * 100) / count_matches, 2)

    rank = get_player_rank(player_data['rank_tier'])

    await message.answer(f'Вы нашли игрока {player_data["profile"]["personaname"]} ({rank})\nВинрейт: {winrate}% ({win_lose['win']} - {win_lose['lose']})', 
                    reply_markup=kb.get_pages())   


    
@router.callback_query(MyCallback.filter(F.foo == 'Матчи'))
async def player_matches(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    recent_matches = get_recent_matches(data['playerId'])

    match_info = []

    for match in recent_matches:
        current_hero = get_current_hero(match['hero_id'])
        is_win = get_is_win(match['radiant_win'], match['player_slot'])
        match_duration = round(match["duration"] / 60)
        match_info.append(f'{is_win} — {match_duration} минут — Герой: {current_hero} — Счет: {match["kills"]}/{match["deaths"]}/{match["assists"]}')

    match_info_str = '\n\n'.join(match_info)
    await callback.message.answer(f'Последние матчи игрока:\n\n{match_info_str}')

@router.callback_query(MyCallback.filter(F.foo == 'Герои'))
async def player_heroes(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    heroes = get_player_heroes(data['playerId'])

    hero_info = []

    for hero in heroes[:5]:
        winrate = round((hero['win'] * 100) / hero['games'], 2)
        hero_name = get_current_hero(hero['hero_id'])
        hero_info.append(f'{hero_name} — Матчей: {hero['games']} — % Винрейт: {winrate}%')
    
    hero_info_str = '\n\n'.join(hero_info)
    await callback.message.answer(f'Сигнатурные герои игрока:\n\n{hero_info_str}')
