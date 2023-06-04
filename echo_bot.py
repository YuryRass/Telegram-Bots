"""Application: EchoBot"""
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()  # for loading Bot-token
bot: Bot = Bot(token=os.getenv('BOT_TOKEN'))
dp: Dispatcher = Dispatcher()


@dp.message(Command(commands=['start']))  # registry of handlers()
async def start_msg(msg: Message):
    """Answer on command /start"""
    await msg.answer('Echo-bot is active!\nEnter any word...')


@dp.message(Command(commands=['help']))
async def help_msg(msg: Message):
    """Answer on command /help"""
    await msg.answer('Bot will simply echo back any message we send it')


@dp.message(F.photo)
async def send_photo(msg: Message):
    """Reply on photo from client"""
    print(msg.photo)
    await msg.reply(msg.photo[0].file_id)


@dp.message()
async def send_msg(msg: Message):
    """Reply on any word from client"""
    await msg.reply(text=msg.text)


if __name__ == "__main__":
    dp.run_polling(bot)
