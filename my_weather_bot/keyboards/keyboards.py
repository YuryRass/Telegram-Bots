"""Модуль для создания пользовательских клавиатур для Telegram бота"""

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
    """
    Клавиаутура с одной клавишей | Меню |, при нажати на которую
    отображается основная клавиатура Telegram бота
    """
    menu_btn = KeyboardButton(text=BOT_BUTTONS['menu'])
    kb_menu: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[menu_btn]],
                                                       resize_keyboard=True)
    return kb_menu


def get_reports_desk(reports: list[WeatherReports],
                     current_page: int) -> InlineKeyboardMarkup | None:
    """
    Инлаин-клавиатура, отображающая историю пользовательских запросов о погоде
    в городах в разное время

    |    <city_1> <date_1 (%d-%m-%Y)>    |
    --------------------------------------
    |    <city_2> <date_2 (%d-%m-%Y)>    |
    --------------------------------------
    |    <city_3> <date_3 (%d-%m-%Y)>    |
    --------------------------------------
    |    <city_4> <date_4 (%d-%m-%Y)>    |
    --------------------------------------
    |Назад| |<page>/<total_page>| |Вперед|
    --------------------------------------

    Предоставляет возможность пагинации. При нажатии на каждую из клавиш
    отправляет соответсвующий callback, который затем
    перехватывается хендлерами.
    Названия callback-ов для клавиш:
    |<city_1> <date_1 (%d-%m-%Y)>| - report_<ID отчета>
    |Назад| - page_back
    |Вперед| - page_next
    |<page>/<total_page>| - not_call (при нажатии не будет происходить
    каких-либо действий)
    """

    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # первые четыре клавиши для получения информации
    # о погоде в некотором городе:
    btns: list[InlineKeyboardButton] = []
    # количество отчетов о погоде на одной странице:
    chunk_size: int = 4
    # список, куда будут помещаться другие списки,
    # каждый из которых хранит четыре отчета о погоде:
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

    # Добавляем эффекты пролистывания страниц,
    # что свойственно для пагинации:
    if current_page == len(splitted_reports):
        kb_builder.row(back_btn, statistic_btn)
    elif current_page == 1:
        kb_builder.row(statistic_btn, next_btn)
    else:
        kb_builder.row(back_btn, statistic_btn, next_btn)

    return kb_builder.as_markup()
