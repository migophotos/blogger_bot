from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.filters import Command

from shared.config import Config
from database.sql import DataBase
from database.user_info import UserInfo
from shared import tools
from handlers.scheduler_manage import set_new_scheduler
from handlers.admin_panel import show_admin_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(msg: Message, bot: Bot):
    db: DataBase = bot.db
    ui = UserInfo(db)
    await ui.init_user_info(msg)  # init user info
    bot.ml.set_lang(ui.get_language())

    start_message = tools.build_start_message(ui, bot.ml)
    await msg.answer(start_message)


@router.message(Command("help"))
async def cmd_start(msg: Message, bot: Bot):
    db: DataBase = bot.db
    ui = UserInfo(db)
    await ui.init_user_info(msg)  # init user info
    bot.ml.set_lang(ui.get_language())

    help_msg = tools.build_help_message(ui, bot.ml)
    await msg.answer(help_msg)


@router.message(Command("profile"))
async def cmd_profile(msg: Message, bot: Bot):
    db: DataBase = bot.db
    ui = UserInfo(db)
    await ui.init_user_info(msg)  # init user info
    bot.ml.set_lang(ui.get_language())

    profile = tools.build_profile_text(ui, bot.ml)
    await msg.answer(profile)


# Attention! This handler should always remain last!
@router.message(F.text)
async def cmd_all_messages(msg: Message, bot: Bot):
    db: DataBase = bot.db
    ui = UserInfo(db)
    await ui.init_user_info(msg)  # init user info
    bot.ml.set_lang(ui.get_language())

    if msg.from_user.is_bot or msg.from_user.id != Config.admin_id:
        warning = bot.ml.msg("no_rights").format(ui.get_first_name())
        await msg.answer(warning)
        return False

    cmd = msg.text.lower()
    if cmd.startswith("cmd:sc"):
        await set_new_scheduler(msg.text, msg)
        return True

    if cmd == 'exit:sc':
        await show_admin_keyboard(msg)
        return True

    await msg.answer(bot.ml.msg("unknown_cmd"))
