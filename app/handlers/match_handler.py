from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from keyboards.player_menu import MyCallback
from aiogram.types import CallbackQuery

from services.dota_api import get_match
from services.current_hero import get_current_hero

from keyboards.match_menu import MyCallback
import keyboards.match_menu as kb

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

        match_duration = round(match_data["duration"] / 60)
        match_winner = ''
        if(match_data['radiant_win']):
            match_winner = 'Победа сил света'
        else:
            match_winner = 'Победа сил тьмы'

        for item in match_data['picks_bans']:
            if not item['is_pick']:
                ban = {'hero': item['hero_id'], 'team': item['team']}
                bans.append(ban)

        for item in match_data['players']:
            player = {
                        'hero': item['hero_id'],
                        'team': item['team_number'],
                        'kills': item['kills'],       
                        'deaths': item['deaths'],
                        'assists': item['assists']          
                    }
            players.append(player)

        await message.answer(f'{match_winner} ({match_duration} минут)\nСилы света: {match_data['radiant_score']} — Cилы тьмы: {match_data['dire_score']}',
                            reply_markup=kb.get_pages())
    else:
        await message.answer('Пожалуйста введите ID матча.')
    
@router.callback_query(MyCallback.filter(F.foo == 'Игроки'))
async def player_heroes(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    match_info = []
    
    for player in players:
        hero = get_current_hero(player['hero'])
        team = 'света' if player['team'] == 0 else 'тьмы'
        kda = f"{player['kills']}/{player['deaths']}/{player['assists']}"
        match_info.append(f'{hero} (Силы {team}) - KDA: {kda}')
        
    match_info_str = '\n\n'.join(match_info)
    await callback.message.answer(f'Игроки матча {data['matchId']}\n\n{match_info_str}')
            
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
        