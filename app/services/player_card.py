import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from services.dota_api import get_win_lose, get_recent_matches
from utils.helpers import get_hero_image, get_player_rank, get_is_win, get_match_duration, get_match_time

chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox") 
chrome_options.add_argument("--disable-dev-shm-usage")  
chrome_options.add_argument("--remote-debugging-port=9222") 
chrome_options.add_argument("--incognito") 
# chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--disable-software-rasterizer")  
chrome_options.add_argument("--disable-extensions") 
chrome_options.add_argument("--no-first-run")  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-dev-shm-usage") 
chrome_options.add_argument('--disable-cache')
chrome_options.add_argument("--disable-web-security")

# For Docker work chromedriver
# chrome_options.binary_location = "/usr/bin/google-chrome-stable"

def create_player_card(id_int32, player_data):
    matches_info = []
    win_lose = get_win_lose(id_int32)

    count_matches = win_lose['win'] + win_lose['lose']
    winrate = round((win_lose['win'] * 100) / count_matches, 2)

    recent_matches = get_recent_matches(id_int32)

    for match in recent_matches:
        is_win = get_is_win(match['radiant_win'], match['player_slot'])

        match_info = {
            'hero_id': match['hero_id'],
            'is_win': is_win,
            'kills': match['kills'],
            'deaths': match['deaths'],
            'assists': match['assists'],
            'duration': match['duration'],
            'average_rank': match['average_rank'],
            'is_win': is_win,
            'start_time': match['start_time']
        }
        matches_info.append(match_info)

    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
            <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: rgb(0, 0, 0);
                font-family: "Noto Sans", sans-serif;
                box-sizing: border-box;
                color: rgb(252, 252, 252);
                display: flex;
                flex-direction: column;
                min-height: 100vh;
            }}
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                background-color: rgb(36, 38, 37);
                padding: 10px 60px;
            }}
            .profile, .rank {{
                display: flex;
                align-items: center;
                gap: 20px;
                font-weight: bold;
            }}
            .profile img {{
                width: 120px;
                border-radius: 50%;
            }}
            .profile_rank {{
                width: 75px;
            }}
            .rank img {{
                width: 40px;
            }}
            .matches {{
                margin: 30px 60px;
                padding: 0 15px;
                background-color: rgb(18, 17, 17);
                border-radius: 5px;
            }}
            .match {{
                display: flex;
                justify-content: space-between;
            }}
            .match img {{
                width: 100px;
                border-radius: 5px;
            }}
            .match_info {{
                display: flex;
                align-items: center;
                gap: 15px
            }}
            .win_icon {{
                background-color: rgb(42, 203, 79);
                color: rgb(0, 0, 0);
                font-weight: 500;
                font-size: 15px;
                border-radius: 4px;
                padding: 10px;
                line-height: 0.5;
                text-align: center;
                justify-content: center;
            }}
            .lose_icon {{
                background-color: rgb(236, 4, 31);
                color: rgb(0, 0, 0);
                font-weight: 500;
                font-size: 15px;
                border-radius: 4px;
                padding: 10px;
                line-height: 0.5;
                text-align: center;
                justify-content: center;
            }}
            .match_kda span {{
            color: rgba(255, 255, 255, 0.36);;  
            }}
            .match_time_info {{
                display: flex;
                align-items: center;
                gap: 10px
            }}
            .match_time_info svg {{
                width: 40px;
            }}
            .match_time_info span {{
                font-size: 12px;
            }}
            .match {{
                margin-bottom: 10px;
            }}
            .match_time span {{
                display: block;
            }}
            </style>
        </head>
        <body>
        <div class="header">
            <div class="profile">
                <img src="{player_data['profile']['avatarfull']}" alt="avatar">
                <div>
                    {player_data['profile']['personaname']}
                </div>
            </div>
            <div class="rank">
                {f"""
                <div>
                    <img src="https://cdn.stratz.com/images/dota2/plus/logo.png" alt="dota_plus" />
                </div>""" if player_data['profile']['plus'] == True else ""}
                <div class="profile_rank">
                    {get_player_rank(player_data['rank_tier'])}
                </div>
            </div>
        </div>
        <div class="matches">
            <h3>Матчи</h3>
            {''.join(f"""
            <div class="match">
                <div class="match_info">
                    <div><img src="{get_hero_image(match['hero_id'])}" alt="" /></div>
                    <span class='{f"win_icon" if match['is_win'] == "П" else "lose_icon"}'>{f"П" if match['is_win'] == "В" else "В"}</span>
                    <div class="match_kda">
                        {match['kills']} <span>/</span> {match['deaths']} <span>/</span> {match['assists']}
                    </div>
                </div>
                <div class="match_time_info">
                    {get_player_rank(match['average_rank'])}
                    <div class="match_time">
                        <span>{get_match_duration(match['duration'])}</span>
                        <span>{get_match_time(match['start_time'])} ч назад</span>
                    </div>
                </div>
            </div>
            """ for match in matches_info)}
        </div>        
        </body>
    </hmtl> 
    """

    #             {winrate}% / {count_matches}

    images_dir = os.path.join('../app/images/') 
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    output_path = os.path.join(images_dir, f'{id_int32}.png')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("data:text/html;charset=utf-8," + html)
    driver.set_window_size(2120, 1080)
    time.sleep(5)
    driver.save_screenshot(output_path)
    driver.quit()