import asyncio
from aiogram import Dispatcher, Bot
from config_data import load_config, Config
from handlers import user_handlers, other_handlers


async def main() -> None:
    config: Config = load_config()
    bot_token: str = config.tg_bot.token
    bot: Bot = Bot(token=bot_token, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
