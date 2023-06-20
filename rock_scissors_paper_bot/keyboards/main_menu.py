from aiogram import Bot
from aiogram.types import BotCommand
from lexicon import LEXICON_COMMANS_RU


async def set_main_menu(bot: Bot) -> None:
    commands: list[BotCommand] = [BotCommand(command=command,
                                             description=description)
                                  for command, description
                                  in LEXICON_COMMANS_RU.items()]
    await bot.set_my_commands(commands=commands)
