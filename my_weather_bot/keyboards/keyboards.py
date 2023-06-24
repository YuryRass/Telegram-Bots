from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lexicon import BOT_BUTTONS


def get_main_menu_kb() -> ReplyKeyboardMarkup:

    """Основная клавиатура для взаимодействия с пользователем:
    -------------------------------------------------
    | Погода в моем городе | Погода в другом городе |
    -------------------------------------------------
    |        История       | Установить свой город  |
    -------------------------------------------------
    """

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


def get_menu_kb() -> ReplyKeyboardMarkup:
    menu_btn = KeyboardButton(text=BOT_BUTTONS['menu'])
    kb_menu: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[menu_btn]],
                                                       resize_keyboard=True)
    return kb_menu