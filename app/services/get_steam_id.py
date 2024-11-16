import requests
import re
from config import STEAM_TOKEN

def extract_steam_id(link):
    username_pattern = r'https://steamcommunity.com/id/([^/]+)/?'      

    username_match = re.match(username_pattern, link)
    if username_match:
        response = requests.get(f'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={STEAM_TOKEN}&vanityurl={username_match.group(1)}')
        steam_data = response.json()
        steam_id = steam_data['response']['steamid']
        return steam_id

    else:
        link = link.rstrip('/')
        steam_id = link.split('/')[-1]

        if steam_id.isdigit():
            return steam_id
        else:
            steam_id = link.split('/')[-2]
            if steam_id.isdigit():
                print(steam_id)
                return steam_id