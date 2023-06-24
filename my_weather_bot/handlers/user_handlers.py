from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import default_state
from keyboards import get_main_menu_kb
from lexicon import bot_welcome_phrase
from database import add_user


router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def start_command(message: Message):
    add_user(str(message.from_user.id))
    main_kb: ReplyKeyboardMarkup = get_main_menu_kb()

    text: str = bot_welcome_phrase(message.from_user.first_name)

    await message.answer(text=text, reply_markup=main_kb)
