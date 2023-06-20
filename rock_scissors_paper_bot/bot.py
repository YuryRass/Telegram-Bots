import asyncio
from aiogram import Dispatcher, Bot
from config_data import load_config, Config
from handlers import user_handlers, other_handlers
from keyboards import set_main_menu

config: Config = load_config()
bot_token: str = config.tg_bot.token
bot: Bot = Bot(token=bot_token, parse_mode='HTML')
dp: Dispatcher = Dispatcher()


async def main() -> None:
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)
    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    dp.startup.register(set_main_menu)
    asyncio.run(main())
