from aiogram import Bot, Router, F
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command


from shared.config import Config
from database.sql import DataBase
from database.user_info import UserInfo
from shared.callback_factory import ContentCbFactory
from shared import tools


import json

router = Router()


@router.callback_query(ContentCbFactory.filter())
async def scheduler_manage(call: CallbackQuery, callback_data: ContentCbFactory, bot: Bot):
    db: DataBase = bot.db
    ui = UserInfo(db)
    await ui.init_user_info(call.message)  # init user info
    bot.ml.set_lang(ui.get_language())

    await call.message.answer("Content Manager....")



