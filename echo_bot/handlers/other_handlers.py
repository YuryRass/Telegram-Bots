from aiogram import Router
from aiogram.types import Message
from lexicon import LEXICON_RU


router: Router = Router()


@router.message()
async def echo_command(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text=LEXICON_RU['no_echo'])