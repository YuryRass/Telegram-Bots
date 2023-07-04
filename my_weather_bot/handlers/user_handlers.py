"""
    Handler, срабатывающий на сообщение /start от пользователя
"""
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
    # добавление пользователя, который отправил сообщение в БД User:
    add_user(str(message.from_user.id))
    # главная клавиатура для пользователя:
    main_kb: ReplyKeyboardMarkup = get_main_menu_kb()

    # приветсвенная фраза от бота:
    await message.answer(text=bot_welcome_phrase(message.from_user.first_name),
                         reply_markup=main_kb)
