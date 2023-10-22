from aiogram.filters.callback_data import CallbackData


class AdminCbFactory(CallbackData, prefix="admin_panel"):
    type: str
    selected: str


class LanguageCbFactory(CallbackData, prefix="change_language"):
    type: str
    selected: str


class SchedulerCbFactory(CallbackData, prefix="scheduler_manage"):
    type: str


class ContentCbFactory(CallbackData, prefix="content_manage"):
    type: str
    selected: str


class ContentTypeCbFactory(CallbackData, prefix="content_manage"):
    selected: str


