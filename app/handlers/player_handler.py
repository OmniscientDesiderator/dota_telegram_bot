from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.player_menu import MyCallback
import keyboards.player_menu as kb

from services.dota_api import get_player_info, get_recent_matches, get_win_lose, get_player_heroes
from services.ranks import get_player_rank
from services.is_win import get_is_win
from services.current_hero import get_current_hero

class Search(StatesGroup):
    playerId = State()
    matchId = State()

router = Router()

@router.message(Command('show_player'))
async def show_player(message: Message, state: FSMContext):
    await state.set_state(Search.playerId)
    await message.answer('Пожалуйста введите Steam ID игрока.')

@router.message(Search.playerId)
async def search_player(message: Message, state: FSMContext):
    await state.update_data(playerId=message.text)
    data = await state.get_data()

    player_data = get_player_info(data['playerId'])
    win_lose = get_win_lose(data['playerId'])

    count_matches = win_lose['win'] + win_lose['lose']
    winrate = round((win_lose['win'] * 100) / count_matches, 2)

    rank = get_player_rank(player_data['rank_tier'])

    await message.answer(f'Вы нашли игрока {player_data["profile"]["personaname"]} ({rank})\nВинрейт: {winrate}% ({win_lose['win']} - {win_lose['lose']})', 
                        reply_markup=kb.get_pages())
    
@router.callback_query(MyCallback.filter(F.foo == 'Матчи'))
async def player_matches(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Последние матчи игрока:')
    data = await state.get_data()

    recent_matches = get_recent_matches(data['playerId'])

    for match in recent_matches:
        current_hero = get_current_hero(match['hero_id'])
        is_win = get_is_win(match['radiant_win'], match['player_slot'])

        match_duration = round(match["duration"] / 60)
        await callback.message.answer(f'{is_win} — {match_duration} минут — Герой: {current_hero} — Счет: {match["kills"]}/{match["deaths"]}/{match["assists"]}')

@router.callback_query(MyCallback.filter(F.foo == 'Герои'))
async def player_heroes(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Сигнатурные герои игрока:')

    data = await state.get_data()

    heroes = get_player_heroes(data['playerId'])

    for hero in heroes[:5]:
        winrate = round((hero['win'] * 100) / hero['games'], 2)
        hero_name = get_current_hero(hero['hero_id'])
        await callback.message.answer(f'{hero_name} — Матчей: {hero['games']} — % Винрейт: {winrate}%')
