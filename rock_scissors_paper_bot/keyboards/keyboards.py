from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon import LEXICON_RU


# Создание клавиатуры согласия сыграть в игру "Камень, ножницы, бумага"
kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

btn_yes: KeyboardButton = KeyboardButton(text=LEXICON_RU['yes_button'])
btn_no: KeyboardButton = KeyboardButton(text=LEXICON_RU['no_button'])

kb_builder.row(btn_yes, btn_no, width=2)
kb_yes_or_no: ReplyKeyboardMarkup = kb_builder.as_markup(
    one_time_keyboard=True, resize_keyboard=True)


# Создание игровой клавиатуры |Камень|Ножницы|Бумага|
btn_rock: KeyboardButton = KeyboardButton(text=LEXICON_RU['rock'])
btn_paper: KeyboardButton = KeyboardButton(text=LEXICON_RU['paper'])
btn_scissors: KeyboardButton = KeyboardButton(text=LEXICON_RU['scissors'])

kb_game: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[btn_rock],
                                                             [btn_scissors],
                                                             [btn_paper]],
                                                   resize_keyboard=True)
