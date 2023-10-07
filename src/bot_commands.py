from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Start bot'),
        BotCommand(command='help', description='Show help info'),
        BotCommand(command='language', description='Change UI Language'),
        BotCommand(command='profile', description='Show my profile'),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
