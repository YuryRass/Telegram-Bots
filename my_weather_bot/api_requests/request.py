from typing import Tuple, List
import requests
from dotenv import load_dotenv
from config import Config, load_config

geo_url = 'https://geocode-maps.yandex.ru/1.x/'
weather_url = 'https://api.weather.yandex.ru/v2/forecast'
load_dotenv()  # загрузка токенов

config: Config = load_config()


def get_weather_coordinates(city: str) -> Tuple[str, str]:
    geo_key: str = config.weather.geo_key
    payload: dict = {'apikey': geo_key, 'geocode': city,
                     'format': 'json'}
    data: dict = requests.get(geo_url, params=payload).json()
    _coords: dict = data['response']['GeoObjectCollection']["featureMember"][0]
    coords: List[str] = _coords["GeoObject"]["Point"]["pos"].split()
    return coords[0], coords[1]  # (широта, долгота)


def get_temp_info(lat, lon) -> dict[str, str]:
    weather_key: str = config.weather.weather_key
    payload: dict = {'lat': lat, 'lon': lon, 'lang': 'ru_RU', 'format': 'json'}
    headers: dict = {'X-Yandex-API-Key': weather_key}
    data: dict = requests.get(weather_url, params=payload,
                              headers=headers).json()
    return data['fact']


def get_weather(city: str) -> dict[str, str] | None:
    try:
        coords: Tuple[str, str] = get_weather_coordinates(city)
    except Exception as e:
        print(e)
        return
    lon, lat = coords
    return get_temp_info(lat, lon)
