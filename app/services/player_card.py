import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from services.dota_api import get_win_lose
from services.ranks import get_player_rank

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
    win_lose = get_win_lose(id_int32)

    count_matches = win_lose['win'] + win_lose['lose']
    winrate = round((win_lose['win'] * 100) / count_matches, 2)

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
            </style>
        </head>
        <body>
            <div class="container">
                {player_data['profile']['personaname']}
                <img src="{player_data['profile']['avatarfull']}" alt="avatar">
                <img src="{get_player_rank(player_data['rank_tier'])}" alt="rank">
                {winrate}% / {count_matches}
            </div>
        </body>
    </hmtl> 
    """

    images_dir = os.path.join('../app/images/') 
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    output_path = os.path.join(images_dir, f'{id_int32}.png')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("data:text/html;charset=utf-8," + html)
    driver.set_window_size(2120, 1080)
    driver.save_screenshot(output_path)
    driver.quit()