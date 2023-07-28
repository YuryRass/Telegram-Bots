import os

BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}


def _get_part_text(text, start, page_size):
    """Функция, возвращающая строку с текстом страницы и ее размер"""
    page_size = min(page_size, len(text) - start)
    text = text[start:start+page_size]
    end_symbs = '.!:;?,'
    counter = 0

    if text[-1] == '.' and text[-2] in end_symbs:
        text = text[:-2]
        page_size -= 2

    for i in range(len(text)-1, 0, -1):
        if text[i] in end_symbs:
            counter = page_size - i - 1
            break

    text = text[:page_size-counter]
    return text, page_size-counter


def prepare_book(path):
    """Функция, формирующая словарь книги"""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    start, count = 0, 1
    while start < len(text):
        page_text, page_size = _get_part_text(text, start, PAGE_SIZE)
        start += page_size
        book[count] = page_text.strip()
        count += 1


# Вызов функции prepare_book для подготовки книги из текстового файла
prepare_book(os.path.join(os.getcwd(), BOOK_PATH))
