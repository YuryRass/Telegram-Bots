from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot():
    token: str


@dataclass
class Config():
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)  # считываем данные с файла .env
    config = Config(tg_bot=TgBot(env('BOT_TOKEN')))
    return config
