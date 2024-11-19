import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager 

from utils.helpers import get_hero_image
from utils.helpers import get_player_rank

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

def truncate_name(name):
    if len(name) > 10:  
        return name[:10] + '...' 
    return name

def create_match_card(match_id, match_data):
    players = []
    bans = []
    match_duration = round(match_data["duration"] / 60)

    for item in match_data['players']:
        personaname = item.get('personaname')
        if personaname is None:
            item['personaname'] = "Private acc"
        player = {
            'personaname': personaname,
            'hero': item['hero_id'],
            'team': item['team_number'],
            'kills': item['kills'],       
            'deaths': item['deaths'],
            'assists': item['assists'],
            'gold': item['gold_spent'],
            'rank': item['rank_tier'],
            'start_time': item['start_time']       
            }
        players.append(player)

    # for ban in match_data['picks_bans']:
    #     if not item['is_pick']:
    #         ban = {'hero': item['hero_id'], 'team': item['team']}
    #         bans.append(ban)

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
                background-color: rgb(10, 10, 10);
                font-family: "Noto Sans", sans-serif;
                box-sizing: border-box;
                color: rgb(252, 252, 252);
                display: flex;
                flex-direction: column;
                min-height: 100vh;
            }}
            .container {{
                background: rgb(47, 49, 51);
                display: flex;
                justify-content: space-between; 
                align-items: center;
                padding: 0 30px;
            }}

            .container h2 {{
                font-size: 60px;
            }}

            .container h4 {{
                font-size: 18px;
            }}

            .center {{
                display: flex;
                align-items: center;
                background: rgb(43, 44, 46);
                border-radius: 10px;
                padding: 5px;
            }}
            .win_team {{
                background: linear-gradient(135deg, rgb(14, 149, 64), rgb(100, 216, 146));
                border-radius: 7px;
                font-size: 12px;
                padding: 6px;
                color: black;
                font-weight: bold;
                text-align: center;
                width: auto;
            }}
            .lost_team {{
                background: linear-gradient(135deg, rgb(218, 50, 16), rgb(212, 129, 73));
                padding: 6px;
                border-radius: 7px;
                font-size: 12px;
                font-weight: bold;
                text-align: center;
            }}
            .score_button {{
                background: rgb(34, 35, 36);
                border-radius: 7px;
                width: 50px;
                text-align: center;
                height: 40px;
                align-items: center;
            }}
            .time_match {{
                width: 70px;
                text-align: center;
                font-size: 15px;
            }}
            .player-card {{
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                width: 100%; 
                text-align: center;
                background-color: rgba(34, 34, 34, 0.7); 
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5); 
                margin-right: 10px;
            }}

            .hero-avatar {{
                width: 100%; 
                height: auto; 
                border-radius: 10px 10px 0 0; 
                margin: 0; 
                padding: 0; 
            }}

            .hero-symbol,
            .score,
            .player-name,
            .player-rank {{
                margin: 15px; 
                padding: 0; 
                color: rgb(252, 252, 252); 
            }}
            .hero-symbol {{
                font-size: 20px; 
            }}
            
            .score {{
                font-size: 20px; 
            }}
            
            .earnings {{
                font-size: 20px; 
            }}
            
            .player-name {{
                font-weight: bold;
                font-size: 20px; 
            }}
            .player-rank {{
                color: rgb(187, 187, 187);
                font-size: 20px; 
            }}

            .player-rank svg {{
                width: 52px;
                height: 52px;
            }}
            
            .team-container {{
                display: flex; 
                align-items: center; 
                justify-content: center; 
            }}
            .left-team {{
                justify-content: flex-start; 
            }}
            .right-team {{
                justify-content: flex-end; 
            }}
            .team {{
                display: flex; 
                flex-direction: row;
                align-items: flex-start; 
            }}
            .vs {{
                margin: 0 20px;
                color: rgb(252, 252, 252); 
                font-size: 28px; 
            }}
            .earnings {{
                font-size: 20px; 
                align-items: center;
            }}

            .earnings-amount {{
                font-weight: bold;
            }}

            .earnings-icon {{
                width: 20px; 
            }}
        
        </style>
    </head>
    <body>
        <div class="container">
            <div>
                <h2>Свет</h2>
                <h4 class="{f"win_team" if match_data["radiant_win"] == 1 else "lost_team"}">{f"Победа" if match_data["radiant_win"] == 1 else "Поражение"}</h4>
            </div>
            <div class="center">
                <div class="score_button"><h3>{match_data['radiant_score']}</h3></div>
                <div class="time_match"><span>{match_duration} минут</span></div>
                <div class="score_button"><h3>{match_data['dire_score']}</h3></div>
            </div>
            <div>
                <h2>Тьма</h2>
                <h4 class="{f"lost_team" if match_data["radiant_win"] == 1 else "win_team"}">{f"Поражение" if match_data["radiant_win"] == 1 else "Победа"}</h4>
            </div>
        </div>
        <div class="container" style="opacity: 70%; padding: 10px 30px">
            <div>Рейтинговая \ All Pick</div>
           
        </div>
        <div style="margin: 40px 40px 0 40px">
            <div class="team-container">
                <div class="team left-team">
                    {''.join(f"""<div class="player-card">
                                    <img src="{get_hero_image(player['hero'])}" alt="Аватар героя" class="hero-avatar">
                                    <div class="score"><b>{player['kills']}</b>&ensp;<span style="color: rgb(97, 94, 94)">/</span>&ensp; <b>{player['deaths']}</b> <span style="color: rgb(97, 94, 94)">&ensp;/</span>&ensp;<b>{player['assists']}</b></div>
                                    <div class="earnings">
                                        <img class="earnings-icon" src="https://stratz.com/images/dota2/gold.png" alt="">
                                        <span class="earnings-amount">{player['gold']}</span>
                                    </div>
                                    <div class="player-name">{truncate_name(str(player['personaname']))}</div>
                                    <div class="player-rank">{get_player_rank(player['rank']) if player['rank'] is not None else "Без звания"}</div>
                                </div>""" for player in players[:5])}
                </div>
                <div class="vs">
                    против
                </div>
                <div class="team right-team">
                   {''.join(f"""<div class="player-card">
                                    <img src="{get_hero_image(player['hero'])}" alt="Аватар героя" class="hero-avatar">
                                    <div class="score"><b>{player['kills']}</b>&ensp;<span style="color: rgb(97, 94, 94)">/</span>&ensp; <b>{player['deaths']}</b> <span style="color: rgb(97, 94, 94)">&ensp;/</span>&ensp;<b>{player['assists']}</b></div>
                                    <div class="earnings">
                                        <img class="earnings-icon" src="https://stratz.com/images/dota2/gold.png" alt="">
                                        <span class="earnings-amount">{player['gold']}</span>
                                    </div>
                                    <div class="player-name">{truncate_name(str(player['personaname']))}</div>
                                    <div class="player-rank">{get_player_rank(player['rank']) if player['rank'] is not None else "Без звания"}</div>
                                </div>""" for player in players[5:])}
                </div>
            </div>
        </div>
    </body>
    </html>
    """ 

    images_dir = os.path.join('../app/images/')
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    output_path = os.path.join(images_dir, f'{match_id}.png')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("data:text/html;charset=utf-8," + html)
    driver.set_window_size(2120, 1080)
    driver.save_screenshot(output_path)
    driver.quit()