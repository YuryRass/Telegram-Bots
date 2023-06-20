from random import choice
from lexicon import LEXICON_RU, USER_WIN_SERIES


def get_bot_choice() -> str:
    choices: list = ['rock', 'scissors', 'paper']
    return LEXICON_RU[choice(seq=choices)]


def get_winner(bot_choice: str, user_choice: str) -> str:
    if bot_choice == user_choice:
        return LEXICON_RU['nobody_won']
    elif (user_choice, bot_choice) in USER_WIN_SERIES:
        return LEXICON_RU['user_won']
    else:
        return LEXICON_RU['bot_won']
