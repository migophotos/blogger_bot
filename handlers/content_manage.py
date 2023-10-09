from aiogram import Bot, Router
from aiogram.types import CallbackQuery

from database.sql import DataBase
from database.user_info import UserInfo
from handlers.callback_factory import ContentCbFactory

router = Router()


@router.callback_query(ContentCbFactory.filter())
async def scheduler_manage(call: CallbackQuery, callback_data: ContentCbFactory, bot: Bot):
    db: DataBase = bot.db
    ui = UserInfo(db)
    await ui.init_user_info(call.message)  # init user info
    bot.ml.set_lang(ui.get_language())

    await call.message.answer("Content Manager....")



