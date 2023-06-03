"""Telegram Bot send photos with cats to each message from clients"""
import os
import time
import requests
from dotenv import load_dotenv


def main():
    """Using parameter 'sendPhoto' from Telegram Bot API"""

    load_dotenv()  # take environment variables from .env
    token: str = os.getenv('BOT_TOKEN')
    tg_url: str = 'https://api.telegram.org'
    photos_url: str = 'https://api.thecatapi.com/v1/images/search'
    max_count: int = 10
    offset: int = -2
    counter: int = 0
    while counter < max_count:
        updates = requests.get(
            f'{tg_url}/bot{token}/getUpdates?offset={offset + 1}',
            timeout=None
        ).json()
        if updates:
            for update in updates['result']:
                _id = update['message']['chat']['id']
                offset = update['update_id']
                photo_links = requests.get(photos_url, timeout=None).json()
                for link in photo_links:
                    url: str = link['url']
                    send_photo_url =\
                        f'{tg_url}/bot{token}/sendPhoto?' + \
                        f'chat_id={_id}&photo={url}'
                    requests.get(send_photo_url, timeout=None)
        counter += 1
        time.sleep(1)


if __name__ == "__main__":
    main()
