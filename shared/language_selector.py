from aiogram import Bot, Router, F
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command

from database.sql import DataBase
from database.user_info import UserInfo
from shared.callback_factory import LanguageCbFactory


router = Router()


@router.message(Command("language"))
async def cmd_language(msg: Message, bot: Bot):
    db: DataBase = bot.db
    ui = UserInfo(db)
    await ui.init_user_info(msg)  # init user info
    bot.ml.set_lang(ui.get_language())

    buttons = [
        InlineKeyboardButton(text="Русский",
                             callback_data=LanguageCbFactory(type="change_language", selected="ru").pack()),
        InlineKeyboardButton(text="English",
                             callback_data=LanguageCbFactory(type="change_language", selected="en").pack()),
        InlineKeyboardButton(text="עברית",
                             callback_data=LanguageCbFactory(type="change_language", selected="he").pack()),
    ]
    kbd = InlineKeyboardBuilder()
    kbd.add(*buttons)
    await msg.answer(text=bot.ml.msg("change_language"), reply_markup=kbd.as_markup())


@router.callback_query(LanguageCbFactory.filter())
async def change_language(call: CallbackQuery, callback_data: LanguageCbFactory, bot: Bot):
    db: DataBase = bot.db
    ui = UserInfo(db)
    await ui.init_user_info(call.message)        # init user info
    bot.ml.set_lang(ui.get_language())

    selected_language = callback_data.selected
    await ui.update_user_info("lang", selected_language)
    bot.ml.set_lang(ui.get_language())
    await call.message.answer(bot.ml.msg("preferred_language"))
    await call.answer()
