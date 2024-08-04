import requests

BASE_URL = 'https://api.opendota.com/api'

def get_player_info(playerId):
    url = f"{BASE_URL}/players/{playerId}"
    response = requests.get(url)
    return response.json()

def get_recent_matches(playerId):
    url = f"{BASE_URL}/players/{playerId}/matches?limit=5"
    response = requests.get(url)
    return response.json()

def get_win_lose(playerId):
    url = f"{BASE_URL}/players/{playerId}/wl"
    response = requests.get(url)
    return response.json()

def get_player_heroes(playerId):
    url = f"{BASE_URL}/players/{playerId}/heroes"
    response = requests.get(url)
    return response.json()

def get_match(matchId):
    url = f"{BASE_URL}/matches/{matchId}"
    response = requests.get(url)
    return response.json()