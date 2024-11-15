import json

hero_json = open('services/dota_heroes.json')
heroes_names = json.load(hero_json)

def get_current_hero(match_hero):
    for hero in heroes_names:
            if match_hero == hero["id"]:
                return hero["localized_name"]