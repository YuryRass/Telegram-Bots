"""
------------------------------Модуль request-----------------------------------
Используется для получения сведений о погоде на сегодня в каком-либо городе.
Для получения метеоданных применяется бесплатный интерфейс 'API Яндекс.Погода',
который использует тестовый ключ weather_key с ограниченнным количеством
запросов.Ключ weather_key присваивается переменной X-Yandex-API-Key,
находящейся в заголовке GET-запроса по получению данных о погоде.
Интерфейс 'API Яндекс.Погода' принимает в качестве параметров только широту
и долготу. Для получения географических координат существующего города
применяется интерфейс 'API Яндекс.Геокодер' посредством бесплатного
ключа geo_key.

Глобальные переменные:
    -- weather_url: str - адрес для получения сведений о погоде.
    После адреса weather_url передаются следующие параметры:
        lat - Широта в градусах. Обязательное поле
        lon - Долгота в градусах. Обязательное поле
        lang - Сочетания языка и страны, для которых будут
    возвращены данные погодных формулировок.
        X-Yandex-API-Key - Значение ключа weather_key (содержится
    в заголовке GET-запроса)

    -- geo_url: str - адрес для получения географических координат
    После адреса geo_url передаются следующие параметры:
        apikey - Ключ API Геокодера (здесь заголовок не нужен,
    как в случае с Яндекс.Погодой)
----------------------------------------------------

Использующиеся методы класса:
    -- _get_weather_coordinates(city: str) -> tuple[str, str] | None -
    возвращает географиеские координаты (широту, долготу) города
    Параметры функции:
    city: str - название города
    Исключения:
    Если информацию о погоде не удалось найти вызывается исключение

    -- _get_temp_info(lat: str, lon: str) -> dict[str, str] - возвращает
    информацию о погоде на сегодня для некоторого города, который
    задается географическими координатами
    Параметры функции:
    lat: str - географическая широта города
    lon: str - географическая долгота города

    -- get_weather(city: str) -> dict[str, str] | None: - возвращает
    информацию о погоде на сегодня для некоторого города
    Параметры функции:
    city: str - название города
"""
from dataclasses import dataclass
import requests
from requests import Response
from config import Config, load_config

geo_url: str = "https://geocode-maps.yandex.ru/1.x/"
weather_url: str = "https://api.weather.yandex.ru/v2/forecast"

# загрузка конфигурационных данных из файла .env:
config: Config = load_config()


@dataclass
class WeatherInCity():

    """Класс для получения сведений о погоде на сегодняшний день в городе"""

    def __init__(self, city: str) -> None:
        self.city = city

    def _get_weather_coordinates(self) -> tuple[str, str] | None:

        """Возвращает географиеские координаты города"""

        geo_key: str = config.weather.geo_key
        payload: dict = {"apikey": geo_key, "geocode": self.city,
                         "format": "json"}
        response: Response = requests.get(geo_url, params=payload, timeout=10)
        if response.status_code != 200:
            return None
        data: dict = response.json()
        _crds: dict = data["response"]["GeoObjectCollection"]["featureMember"]
        coords: list[str] = _crds[0]["GeoObject"]["Point"]["pos"].split()
        return coords[0], coords[1]  # (широта, долгота)

    def _get_temp_info(self, lat: str, lon: str) -> dict[str, str]:

        """Возвращает информацию о погоде на сегодня для некоторого города,
        который задается географическими координатами
        """

        weather_key: str = config.weather.weather_key
        payload: dict = {"lat": lat, "lon": lon, "lang": "ru_RU",
                         "format": "json"}
        headers: dict = {"X-Yandex-API-Key": weather_key}
        data: dict = requests.get(weather_url, params=payload,
                                  headers=headers, timeout=10).json()
        return data["fact"]

    def get_weather(self) -> dict[str, str] | None:

        """Возвращает информацию о погоде на сегодня для некоторого города"""

        coords: tuple[str, str] = self._get_weather_coordinates()
        if not coords:
            return None
        lon, lat = coords
        return self._get_temp_info(lat, lon)
