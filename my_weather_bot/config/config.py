"""
Модуль congig.py предназначен для загрузки конфигурационной информации
для подключения к базе данной PostgreSQL и работы Telegram-бота
"""
from dataclasses import dataclass
from environs import Env


@dataclass
class DataBase():
    """
    База данных PostgreSQL
    Атрибуты:
    1. user_name: str - имя пользователя для подключения к БД
    2. user_password: str - пароль для пользователя
    3. address: str - адрес, по которому осуществляется подключение к БД
    """
    user_name: str
    user_passsword: str
    address: str


@dataclass
class WeatherData():
    """
    Данные о погоде
    Атрибуты:
    1. geo_key: str - ключ для использования интерфейса 'API Яндекс.Геокодер'
    2. weather_key: str - ключ для 'API Яндекс.Погода'
    """
    geo_key: str
    weather_key: str


@dataclass
class Bot():
    """
    Бот: My_weather_bot
    Атрибут bot_token: str - уникальный номер для идентификации бота
    """
    bot_token: str


@dataclass
class Config():
    """
    Класс конфигураций.
    Хранит всю конфигурационную информацию для работы
    Telegram бота, подключения к базе данных и получения сведений о погоде
    """
    db: DataBase
    weather: WeatherData
    bot: Bot


def load_config(path: str | None = None) -> Config:
    """
    Функция предназначена для загрузки конфиденциальной информации
    из файла '.env' для корректной работы бота My_weather_bot
    """
    env = Env()
    env.read_env(path)  # чтения информации из файла .env
    config: Config = Config(db=DataBase(user_name=env('DB_USER'),
                                        user_passsword=env('DB_PASSWORD'),
                                        address=env('DB_ADDRESS')),
                            weather=WeatherData(geo_key=env('GEO_KEY'),
                            weather_key=env('WEATHER_KEY')),
                            bot=Bot(bot_token=env('BOT_TOKEN')))
    return config
