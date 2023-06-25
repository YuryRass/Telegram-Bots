import asyncio
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from config import load_config, Config
from handlers import user_handlers, other_handlers, callback_handlers


async def main():
    storage: MemoryStorage = MemoryStorage()
    dp: Dispatcher = Dispatcher(storage=storage)
    config: Config = load_config()
    bot: Bot = Bot(token=config.bot.bot_token)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)
    dp.include_router(callback_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    dp.run_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
