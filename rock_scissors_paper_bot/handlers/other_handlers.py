from aiogram import Router
from aiogram.types import Message
from lexicon import LEXICON_RU


router: Router = Router()


@router.message()
async def send_answer(message: Message):
    await message.answer(LEXICON_RU['other_answer'])
