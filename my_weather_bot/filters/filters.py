from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from lexicon import BOT_BUTTONS


class IsNextOrBackClick(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data in [BOT_BUTTONS['back'], BOT_BUTTONS['next']]


class IsNotCallClick(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == BOT_BUTTONS['not_call']


class IsCityReport(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.split('_')[0] == 'report'
