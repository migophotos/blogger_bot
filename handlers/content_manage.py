from aiogram import Bot, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.sql import DataBase
from database.user_info import UserInfo
from handlers.callback_factory import ContentCbFactory, ContentTypeCbFactory, PromptConfigCb
from shared.messages import MultiLang
from shared.config import Config

from handlers.admin_panel import show_admin_keyboard

router = Router()


@router.callback_query(ContentCbFactory.filter())
async def change_content(call: CallbackQuery, callback_data: ContentCbFactory, bot: Bot):
    db: DataBase = bot.db
    ui = UserInfo(db)
    await ui.init_user_info(call.message)  # init user info
    ml: MultiLang = bot.ml
    ml.set_lang(ui.get_language())

    buttons = [
        InlineKeyboardButton(text=ml.msg("openai"),
                             callback_data=ContentTypeCbFactory(type="content_selector", selected="openai").pack()),
        InlineKeyboardButton(text=ml.msg("external_csv"),
                             callback_data=ContentTypeCbFactory(type="content_selector", selected="external_csv").pack()),
        InlineKeyboardButton(text=ml.msg("external_json"),
                             callback_data=ContentTypeCbFactory(type="content_selector", selected="external_json").pack()),
        InlineKeyboardButton(text=ml.msg("back_to_admin"),
                             callback_data=ContentTypeCbFactory(type="content_selector", selected="back_to_admin").pack()),
    ]
    kbd = InlineKeyboardBuilder()
    kbd.add(*buttons)
    kbd.adjust(1)
    await call.message.answer(text=ml.msg("select_content_type"), reply_markup=kbd.as_markup())
    await call.answer()


def prompt_selector_kb(ml: MultiLang):
    buttons = [
        InlineKeyboardButton(text=ml.msg("ru_prompt"), callback_data=PromptConfigCb(selected_prompt="ru").pack()),
        InlineKeyboardButton(text=ml.msg("en_prompt"), callback_data=PromptConfigCb(selected_prompt="en").pack()),
        InlineKeyboardButton(text=ml.msg("he_prompt"), callback_data=PromptConfigCb(selected_prompt="he").pack())
    ]
    kbd = InlineKeyboardBuilder()
    kbd.add(*buttons)
    kbd.adjust(1)
    return kbd


@router.callback_query(ContentTypeCbFactory.filter())
async def content_selector(call: CallbackQuery, callback_data: ContentTypeCbFactory, bot: Bot):
    db: DataBase = bot.db
    ui = UserInfo(db)
    await ui.init_user_info(call.message)        # init user info
    ml: MultiLang = bot.ml
    ml.set_lang(ui.get_language())

    content_type = callback_data.selected
    if content_type == 'back_to_admin':
        await show_admin_keyboard(call.message, is_answer=False)
        return

    await db.update_user(ui.get_id(), "content_type", content_type)
    if content_type == 'openai':
        prompt_selector_kb(ml)
    elif content_type == 'external_csv':
        pass
    elif content_type == 'external_json':
        pass

    await call.answer()
