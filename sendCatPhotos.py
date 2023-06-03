# import requests
import os
import time
import requests
from dotenv import load_dotenv


load_dotenv()  # take environment variables from .env
TOKEN = os.getenv('BOT_TOKEN')
TG_URL = 'https://api.telegram.org'
CAT_PHOTOS_URL = 'https://api.thecatapi.com/v1/images/search'
MAX_COUNT = 10
offset = -2
counter = 0


while counter < MAX_COUNT:
    updates = requests.get(
        f'{TG_URL}/bot{TOKEN}/getUpdates?offset={offset + 1}'
    ).json()
    if updates:
        for update in updates['result']:
            id = update['message']['chat']['id']
            offset = update['update_id']
            photo_links = requests.get(
                'https://api.thecatapi.com/v1/images/search'
            ).json()
            for link in photo_links:
                url = link['url']
                requests.get(
                    f'{TG_URL}/bot{TOKEN}/sendPhoto?chat_id={id}&photo={url}'
                )
    counter += 1
    time.sleep(1)
