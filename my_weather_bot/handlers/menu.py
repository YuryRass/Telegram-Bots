from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lexicon import BOT_PHRASE, BOT_BUTTONS


async def bot_welcome_phrase(first_name: str):
    return f'Привет {first_name}, ' + BOT_PHRASE['welcome']


async def get_main_menu() -> ReplyKeyboardMarkup:
    btn1: KeyboardButton = KeyboardButton(
        text=BOT_BUTTONS['weather_in_my_city'])
    btn2: KeyboardButton = KeyboardButton(
        text=BOT_BUTTONS['weather_in_other_city'])
    btn3: KeyboardButton = KeyboardButton(
        text=BOT_BUTTONS['history'])
    btn4: KeyboardButton = KeyboardButton(
        text=BOT_BUTTONS['set_your_city'])

    keyboard = ReplyKeyboardMarkup(keyboard=[[btn1, btn2], [btn3, btn4]],
                                   resize_keyboard=True,
                                   one_time_keyboard=True)
    return keyboard