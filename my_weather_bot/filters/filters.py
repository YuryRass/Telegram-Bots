"""
    Модуль filters описывает три класса для
    отлавливания callback-ов роутерами
"""
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from lexicon import BOT_BUTTONS


class IsNextOrBackClick(BaseFilter):
    """
        Проверка на callback при нажатии
        на клавиши "Назад" или "Вперёд"
    """
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data in [BOT_BUTTONS['back'], BOT_BUTTONS['next']]


class IsNotCallClick(BaseFilter):
    """
        Проверка на callback при нажатии на клавишу, которая
        ничего не отображает
    """
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == BOT_BUTTONS['not_call']


class IsCityReport(BaseFilter):
    """
        Проверка на callback при нажатии на клавишу, выдающую
        полный отчет о погоде в конкретном городе
    """
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.split('_')[0] == 'report'
