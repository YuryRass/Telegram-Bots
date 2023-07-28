from copy import deepcopy
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import InlineKeyboardMarkup, CallbackQuery
from lexicon.lexicon import LEXICON
from database.database import users_db, user_dict_template
from services.file_handling import book
from keyboards.pagination_kb import create_pagination_keyboard
from keyboards.bookmarks_kb import create_bookmarks_keyboard, \
    create_edit_keyboard
from filters.filters import IsDigitCallbackData, IsDelBookmarkCallbackData

router: Router = Router()


@router.message(CommandStart())
async def proccess_start_command(message: Message):
    """Этот хэндлер будет срабатывать на команду "/start" -
       добавлять пользователя в базу данных, если его там еще не было
       и отправлять ему приветственное сообщение
    """
    await message.answer(text=LEXICON['/start'])

    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)


@router.message(Command(commands='help'))
async def proccess_help_command(message: Message):
    """Этот хэндлер будет срабатывать на команду "/help"
    и отправлять пользователю сообщение со списком доступных команд в боте
    """
    await message.answer(text=LEXICON['/help'])


@router.message(Command(commands='beginning'))
async def proccess_beginning_command(message: Message):
    """Этот хэндлер будет срабатывать на команду "/beginning"
       и отправлять пользователю первую страницу книги с кнопками пагинации
    """
    users_db[message.from_user.id]['page'] = 1
    beginning_text: str = book[1]
    beginning_kb: InlineKeyboardMarkup = create_pagination_keyboard(
        'backward', f'1/{len(book)}', 'forward'
    )
    await message.answer(text=beginning_text,
                         reply_markup=beginning_kb)


@router.message(Command(commands='continue'))
async def proccess_continue_command(message: Message):
    """Этот хэндлер будет срабатывать на команду "/continue"
       и отправлять пользователю страницу книги, на которой пользователь
       остановился в процессе взаимодействия с ботом
    """
    page_num: int = users_db[message.from_user.id]['page']
    book_text: str = book[page_num]
    continue_kb: InlineKeyboardMarkup = create_pagination_keyboard(
        'backward', f'{page_num}/{len(book)}', 'forward'
    )
    await message.answer(text=book_text,
                         reply_markup=continue_kb)


@router.message(Command(commands='bookmarks'))
async def proccess_bookmarks_command(message: Message):
    """Этот хэндлер будет срабатывать на команду "/bookmarks"
       и отправлять пользователю список сохраненных закладок,
       если они есть или сообщение о том, что закладок нет
    """
    if users_db[message.from_user.id]['bookmarks']:
        if users_db[message.from_user.id]["bookmarks"]:
            await message.answer(
                text=LEXICON[message.text],
                reply_markup=create_bookmarks_keyboard(
                    *users_db[message.from_user.id]["bookmarks"]))
        else:
            await message.answer(text=LEXICON['no_bookmarks'])


@router.callback_query(Text(text='forward'))
async def process_forward_press(callback: CallbackQuery):
    """Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
       во время взаимодействия пользователя с сообщением-книгой
    """
    if users_db[callback.from_user.id]['page'] < len(book):
        users_db[callback.from_user.id]['page'] += 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                    'forward'))
    await callback.answer()


@router.callback_query(Text(text='backward'))
async def process_backward_press(callback: CallbackQuery):
    """Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
       во время взаимодействия пользователя с сообщением-книгой
    """
    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -= 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
                text=text,
                reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                    'forward'))
    await callback.answer()


@router.callback_query(lambda x: '/' in x.data
                       and x.data.replace('/', '').isdigit())
async def process_page_press(callback: CallbackQuery):
    """Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
       и с номером текущей страницы и добавлять текущую страницу в закладки
    """
    users_db[callback.from_user.id]['bookmarks'].add(
        users_db[callback.from_user.id]['page'])
    await callback.answer('Страница добавлена в закладки!')


@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery):
    """Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
       с закладкой из списка закладок
    """
    text = book[int(callback.data)]
    users_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(
                text=text,
                reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                    'forward'))
    await callback.answer()


@router.callback_query(Text(text='edit_bookmarks'))
async def process_edit_press(callback: CallbackQuery):
    """Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
       "редактировать" под списком закладок
    """
    await callback.message.edit_text(
                text=LEXICON[callback.data],
                reply_markup=create_edit_keyboard(
                                *users_db[callback.from_user.id]["bookmarks"]))
    await callback.answer()


@router.callback_query(Text(text='cancel'))
async def process_cancel_press(callback: CallbackQuery):
    """Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
       "отменить" во время работы со списком закладок
       (просмотр и редактирование)
    """
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()


@router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmark_press(callback: CallbackQuery):
    """Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
       с закладкой из списка закладок к удалению
    """
    users_db[callback.from_user.id]['bookmarks'].remove(
                                                    int(callback.data[:-3]))
    if users_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
                    text=LEXICON['/bookmarks'],
                    reply_markup=create_edit_keyboard(
                            *users_db[callback.from_user.id]["bookmarks"]))
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
    await callback.answer()
