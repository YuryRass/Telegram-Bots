from environs import Env
from dataclasses import dataclass


@dataclass
class DataBase():
    user_name: str
    user_passsword: str
    address: str


@dataclass
class WeatherData():
    geo_key: str
    weather_key: str


@dataclass
class Bot():
    bot_token: str


@dataclass
class Config():
    db: DataBase
    weather: WeatherData
    bot: Bot


def load_config(path: str | None = None):
    env = Env()
    env.read_env(path)
    config = Config(db=DataBase(user_name=env('DB_USER'),
                                user_passsword=env('DB_PASSWORD'),
                                address=env('DB_ADDRESS')),
                    weather=WeatherData(geo_key=env('GEO_KEY'),
                                        weather_key=env('WEATHER_KEY')),
                    bot=Bot(bot_token=env('BOT_TOKEN')))
    return config