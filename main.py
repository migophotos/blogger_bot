from aiogram import Bot, Dispatcher
import asyncio
import logging

from database.sql import DataBase
from shared.config import Config
from shared.messages import MultiLang
from src.bot_commands import set_commands
from src import commands
from shared import language_selector, scheduler_manage, admin_panel, content_manage
from shared.content_provider import ContentProvider


async def start_bot(bot: Bot):
    # open connection to database and store it in bot!
    db = DataBase(Config.db_path)
    await db.create_tables()
    await db.insert_def_scheduler()

    await bot.send_message(Config.admin_id, text=f'Bot {Config.bot_name} started!')
    await set_commands(bot)
    # let's feint with our ears...
    bot.ml = MultiLang(db)
    bot.db = db
    bot.provider = ContentProvider(bot)
    next_run = await bot.provider.restart_scheduler()
    await bot.send_message(Config.admin_id, text=f'Content Provider Job started.\nNext run at: {next_run}')


async def stop_bot(bot: Bot):
    # close connection to my database
    db: DataBase = bot.db
    await db.disconnect()
    await bot.send_message(Config.admin_id, text=f'Bot {Config.bot_name} stopped!')


async def start():
    # logging.basicConfig(
    #     level=logging.ERROR)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    bot = Bot(token=Config.bot_token, parse_mode='HTML')
    dp = Dispatcher()

    # register start/stop handlers
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    # route commands
    dp.include_router(language_selector.router)
    dp.include_router(admin_panel.router)
    dp.include_router(scheduler_manage.router)
    dp.include_router(content_manage.router)
    # Attention! commands router should always remain last!
    dp.include_router(commands.router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())
