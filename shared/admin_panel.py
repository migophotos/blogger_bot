from aiogram import Bot, Router, F
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command


from shared.config import Config
from database.sql import DataBase
from database.user_info import UserInfo
from shared.callback_factory import AdminCbFactory, SchedulerCbFactory, ContentCbFactory
from shared import tools

import json

router = Router()


@router.message(Command("admin"))
async def cmd_admin(msg: Message, bot: Bot):
    db: DataBase = bot.db
    ui = UserInfo(db)
    await ui.init_user_info(msg)  # init user info
    bot.ml.set_lang(ui.get_language())

    if msg.from_user.is_bot or msg.from_user.id != Config.admin_id:
        warning = bot.ml.msg("no_rights").format(ui.get_first_name())
        await msg.answer(warning)
        return

    await show_keyboard(msg)


async def show_keyboard(msg: Message):
    buttons = [InlineKeyboardButton(text=msg.bot.ml.msg("scheduler_manage"),
                                    callback_data=SchedulerCbFactory(type="scheduler_manage").pack()),
               InlineKeyboardButton(text=msg.bot.ml.msg("content_manage"),
                                    callback_data=ContentCbFactory(type="content_manage", selected="").pack()),
               InlineKeyboardButton(text=msg.bot.ml.msg("stop_scheduler"),
                                    callback_data=AdminCbFactory(type="stop_scheduler", selected="").pack()),
               InlineKeyboardButton(text=msg.bot.ml.msg("restart_scheduler"),
                                    callback_data=AdminCbFactory(type="restart_scheduler", selected="").pack()),
               ]
    kbd = InlineKeyboardBuilder()
    kbd.add(*buttons)
    kbd.adjust(1)
    await msg.answer(text=msg.bot.ml.msg("admin_panel"), reply_markup=kbd.as_markup())


@router.callback_query(AdminCbFactory.filter())
async def restart_scheduler(call: CallbackQuery, callback_data: AdminCbFactory, bot: Bot):
    db: DataBase = bot.db
    ui = UserInfo(db)
    await ui.init_user_info(call.message)  # init user info
    bot.ml.set_lang(ui.get_language())

    if callback_data.type == "stop_scheduler":
        job_status = await bot.provider.stop_scheduler()
        await call.message.answer(f"Content provider job {job_status}")

    if callback_data.type == "restart_scheduler":
        next_run = await bot.provider.restart_scheduler()
        await call.message.answer(f"Content provider job restarted.\nNext run at: {next_run}")
