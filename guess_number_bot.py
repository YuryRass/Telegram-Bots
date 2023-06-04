"""Однопользовательский бот, реализующий игру 'Угадай число'"""
import os
import random
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Text, Command


load_dotenv()  # загрузка токена для бота
bot_token: str = os.getenv('BOT_TOKEN')

# Создаем объекты бота и диспетчера
bot: Bot = Bot(bot_token)
dp: Dispatcher = Dispatcher()

# Количество попыток, доступных пользователю в игре
attempts: int = 5

# Словарь, в котором будут храниться данные пользователя
user: dict = {'in_game': False,
              'secret_number': None,
              'attempts': 0,
              'total_games': 0,
              'wins': 0}

# Ответы пользователя на предложение поиграть в игру
agree_to_play = ['Да', 'Давай', 'Сыграем', 'Давай сыграем']
disagree_to_play = ['Нет', 'Не сыграем', 'Не хочу', 'Не', 'Неа']


def get_random_number() -> int:
    """Функция, возвращающая случайное целое число от 1 до 100"""
    return random.randint(1, 100)


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    """Этот хэндлер будет срабатывать на команду /start"""

    await message.answer('Привет!\nДавай сыграем в игру "Угадай число"?\n\n'
                         'Чтобы получить правила игры и список доступных '
                         'команд - отправьте команду /help')


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    """Этот хэндлер будет срабатывать на команду /help"""

    await message.answer(f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
                         f'а вам нужно его угадать\nУ вас есть {attempts} '
                         f'попыток\n\nДоступные команды:\n/help - правила '
                         f'игры и список команд\n/cancel - выйти из игры\n'
                         f'/stat - посмотреть статистику\n\nДавай сыграем?')


@dp.message(Command(commands=['cancel']))
async def quit_game(message: Message):
    """Хэндлер по выходу из игры"""

    if user['in_game']:
        await message.answer("Вы вышли из игры!")
        user['in_game'] = False
        user['total_games'] -= 1
    else:
        await message.answer('А вы и так не в игре\n'
                             'Может сыграем?')


@dp.message(Command(commands=['stat']))
async def print_stat(message: Message):
    """Вывод на печать статистики игрока"""
    await message.answer(f'Ваша статистика:\n'
                         f'- количество игр: {user["total_games"]}\n'
                         f'- количество побед: {user["wins"]}\n')


@dp.message(Text(text=agree_to_play, ignore_case=True),
            lambda _: not user['in_game'])
async def start_play(message: Message):
    """Хэндлер по старту игры 'Угадай число'"""

    user['in_game'] = True
    user['total_games'] += 1
    user['secret_number'] = get_random_number()
    await message.answer('И вот игра началась\n'
                         'Напишите число от 1 до 100\n')


@dp.message(Text(text=disagree_to_play, ignore_case=True),
            lambda _: not user['in_game'])
async def play_later(message: Message):
    """Хэндлер по обработке отрицательного ответа от пользователя"""

    await message.answer(f'Когда захотите сыграть в игру напишите боту '
                         f'один из вариантов ответа: {agree_to_play}')


@dp.message(lambda x: x.text and x.text.isdigit()
            and int(x.text) in range(1, 101))
async def game(message: Message):
    """Основной хэндлер, реализующий игру 'Угадай число'"""
    if user['in_game']:
        num: int = int(message.text)
        user['attempts'] += 1
        if num == user['secret_number']:
            user['in_game'] = False
            user['wins'] += 1
            user['attempts'] = 0
            await message.answer('Победа! Вы отгадали число\n'
                                 'Хотите сыграть еще раз?')
        elif num < user['secret_number']:
            await message.answer('Введенное число меньше загаданного')
        else:
            await message.answer('Введенное число больше загаданного')

        if user['attempts'] == attempts:
            user['in_game'] = False
            user['attempts'] = 0
            await message.answer(f'Вы проиграли, потратив все попытки\n'
                                 f'{user["secret_number"]} - загаданное число'
                                 f'\nМожет хотите сыграть еще раз?')
    else:
        await message.answer('Вы еще не начали игру!\n'
                             'Может сыграем?')


@dp.message(lambda _: user['in_game'])
async def incorrect_input_value_in_game(message: Message):
    """Хэндлер по обработке некорректных значений в игре"""

    await message.answer('Вы ввели некорректное значение\n'
                         'Необходимо ввести натуральное число от 1 до 100')


@dp.message()
async def incorrect_input(message: Message):
    """Хэндлер по обработке некорректных значений"""

    await message.answer(f"Введено некоректное значение\n"
                         f"Если Вы хотите сыграть в игру, "
                         f"введите один из вариантов: {agree_to_play}")


if __name__ == "__main__":
    dp.run_polling(bot)
