from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Text, Command
from lexicon import LEXICON_RU
from keyboards import kb_yes_or_no, kb_game
from services import get_bot_choice, get_winner


router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'],
                         reply_markup=kb_yes_or_no)


@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'],
                         reply_markup=kb_yes_or_no)


@router.message(Command(commands=['delmenu']))
async def process_delete_menu(message: Message, bot: Bot):
    await bot.delete_my_commands()
    await message.answer(text='Кнопка "Menu" удалена')


@router.message(Text(text=LEXICON_RU['yes_button']))
async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['yes'], reply_markup=kb_game)


@router.message(Text(text=LEXICON_RU['no_button']))
async def process_no_answer(message: Message):
    await message.answer(text=LEXICON_RU['no'])


@router.message(Text(text=[LEXICON_RU['rock'],
                           LEXICON_RU['scissors'],
                           LEXICON_RU['paper']]))
async def process_game_button(message: Message):
    bot_choice: str = get_bot_choice()
    await message.answer(text=f'{LEXICON_RU["bot_choice"]} - ' +
                         f'{bot_choice}')
    user_choice: str = message.text
    winner: str = get_winner(bot_choice, user_choice)
    await message.answer(text=winner, reply_markup=kb_yes_or_no)
