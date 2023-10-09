from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_bot_name(bot: Bot):
    '''
        Set Name, Short description, Description, and Commands list for the given user language
        "the bot's" name. 0-64 characters,
    '''
    data = [
        (
            'Blogger Bot',
            "en",
        ),
        (
            'Блогер-Бот',
            "ru",
        ),
        (
            'בוט בלוגר',
            "he",
        )
    ]
    for name, language in data:
        bot_name = await bot.get_my_name(language_code=language)
        if bot_name and bot_name.name != name:
            await bot.set_my_name(name=name, language_code=language)


async def set_commands(bot: Bot):
    '''
        Set Short description, Description, and Commands list for the given user language
        "the bot's" name. 0-64 characters,
        "the bot's" short description, which is shown on the bot's profile page and is sent together with the link
                    when users share the bot. 0-120 characters.
        "the bot's" description, which is shown in the chat with the bot if the chat is empty. 0-512 characters.
        "A two-letter" ISO 639-1 language code"
        "the list" of the bot's commands
        "the scope" - BotCommandScope JSON-serialized object, describing scope of users for which the commands are relevant
    '''
    data = [
        (
            'Blogger Bot',
            "Bot for sending messages",
            "Bot for sending messages",
            "en",
            [
                BotCommand(command='start', description='Start bot'),
                BotCommand(command='help', description='Show help info'),
                BotCommand(command='language', description='Change UI Language'),
                BotCommand(command='profile', description='Show my profile'),
                BotCommand(command='admin', description='Change Settings (for administrator only)')
            ],
            BotCommandScopeDefault(),
        ),
        (
            'Блогер-Бот',
            "Бот для рассылки сообщений",
            "Бот для рассылки сообщений",
            "ru",
            [
                BotCommand(command='start', description='Запуск бота'),
                BotCommand(command='help', description='Помощь'),
                BotCommand(command='language', description='Смена языка'),
                BotCommand(command='profile', description='Показать профиль'),
                BotCommand(command='admin', description='Изменить настройки (только для администратора)')
            ],
            BotCommandScopeDefault(),
        ),
        (
            'בוט בלוגר',
            "בוט לשליחת הודעות",
            "בוט לשליחת הודעות",
            "he",
            [
                BotCommand(command='start', description='התחל בוט'),
                BotCommand(command='help', description='הצג מידע עזרה'),
                BotCommand(command='language', description='שנה שפת ממשק משתמש'),
                BotCommand(command='profile', description='הצג את הפרופיל שלי'),
                BotCommand(command='admin', description='שנה הגדרות (למנהל בלבד)')
            ],
            BotCommandScopeDefault(),
        )
    ]
    for name, short_descr, description, language, commands_list, commands_scope in data:
        await bot.set_my_short_description(short_description=short_descr, language_code=language)
        await bot.set_my_description(description=description, language_code=language)
        await bot.set_my_commands(commands=commands_list, scope=commands_scope, language_code=language)


