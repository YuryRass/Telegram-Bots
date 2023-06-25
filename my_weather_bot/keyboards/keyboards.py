from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon import BOT_BUTTONS
from database import WeatherReports


def get_main_menu_kb() -> ReplyKeyboardMarkup:

    """Основная клавиатура для взаимодействия с пользователем:
    -------------------------------------------------
    | Погода в моем городе | Погода в другом городе |
    -------------------------------------------------
    |        История       | Установить свой город  |
    -----------------------------------------------
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


def get_reports_desk(reports: list[WeatherReports],
                     current_page: int) -> InlineKeyboardMarkup | None:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    btns: list[InlineKeyboardButton] = []
    chunk_size: int = 4
    splitted_reports = list()
    for i in range(0, len(reports), chunk_size):
        splitted_reports.append(reports[i:i+chunk_size])

    if current_page > len(splitted_reports) or current_page < 1:
        return None

    for report in splitted_reports[current_page - 1]:
        btn_text: str = f'{report.city} {report.date.strftime("%d-%m-%Y")}'
        btns.append(InlineKeyboardButton(
            text=btn_text, callback_data=f'report_{report.id}'))

    kb_builder.row(*btns, width=1)

    statistic_btn: InlineKeyboardButton = InlineKeyboardButton(
        text=f'{current_page}/{len(splitted_reports)}',
        callback_data=BOT_BUTTONS['not_call'])

    back_btn: InlineKeyboardButton = InlineKeyboardButton(
        text='Назад', callback_data=BOT_BUTTONS['back'])

    next_btn: InlineKeyboardButton = InlineKeyboardButton(
        text='Вперёд', callback_data=BOT_BUTTONS['next'])

    if current_page == len(splitted_reports):
        kb_builder.row(back_btn, statistic_btn)
    elif current_page == 1:
        kb_builder.row(statistic_btn, next_btn)
    else:
        kb_builder.row(back_btn, statistic_btn, next_btn)

    return kb_builder.as_markup()
