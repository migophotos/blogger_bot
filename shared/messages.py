from database.sql import DataBase


MESSAGES_RU = {
    "hello": "Здравствуйте",
    "your_role": "Ваша роль",
    "your_lang": "Язык общения",
    "your_id": "Ваш код",
    "channel_invitation": "Подпишитесь на каналы {0} для получениия информации о продукции компании и скидках",
    "about_bot": 'Этот бот содержит полную информацию о продукции компании <b>"Our Company"</b>',
    "admin_text": 'Используйте команду /admin для установки времени отправки сообщений и управления сообщениями',
    "preferred_language": 'Вы выбрали Русский язык, выполните команду /profile для проверки',
    "change_language": 'Выберите Язык Общения',
    "no_rights": '<b>Здравствуйте {0}!</b>\nК сожалению у вас нет прав доступа к этой команде....\n<b>Досвидания!</b>',
    "admin_panel": 'Панель администратора',
    "scheduler_manage": 'Планировщик...',
    "content_manage": 'Контент...',
    "start_scheduler": 'Запустить планировщик',
    "restart_scheduler": 'Перезапустить планировщик',
    "stop_scheduler": 'Остановить планировщик',
    "unknown_cmd": 'Неизвестная команда, проверьте синтаксис!',
    "select_content_type": 'Выберите тип контента',
    "openai": 'Автоматически генерировать с помощью OpenAI',
    "external_csv": 'Внешний CSV-файл',
    "external_json": 'Внешний JSON файл',
    "back_to_admin": 'Вернуться в панель администратора',
}

MESSAGES_EN = {
    "hello": "Hello",
    "your_role": "Your role",
    "your_lang": "Your language",
    "your_id": "Your ID",
    "channel_invitation": "Subscribe to the channel {0} for information about the company's products and discounts",
    "about_bot": 'This bot contains complete information about <b>"Our Company"</b>',
    "admin_text": 'Use the /admin command to set the time of sending messages and to manage messages',
    "preferred_language": 'You have selected an English language, run the /profile command to check',
    "change_language": 'Select Language of Communication',
    "no_rights": '<b>Hello {0}!</b>\nUnfortunately, you do not have access rights to this command....\n<b>Goodbye!</b>',
    "admin_panel": 'Admin Panel',
    "scheduler_manage": 'Scheduler...',
    "content_manage": 'Content...',
    "start_scheduler": 'Start Scheduler',
    "restart_scheduler": 'Restart Scheduler',
    "stop_scheduler": 'Stop Scheduler',
    "unknown_cmd": 'Unknown command, check the syntax!',
    "select_content_type": 'Select content type',
    "openai": 'Automatically generate with OpenAI',
    "external_csv": 'External CSV file',
    "external_json": 'External JSON file',
    "back_to_admin": 'Return to Admin panel',
}

MESSAGES_HE = {
    "hello": "שלום",
    "your_role": "התפקיד שלך",
    "your_lang": "שפת התקשורת",
    "your_id": "הקוד שלך",
    "channel_invitation": "הירשם לערוץ {0} לקבלת מידע על מוצרי החברה וההנחות",
    "about_bot": 'בוט זה מכיל מידע מלא על מוצרי החברה<b>"Our Company"</b>',
    "admin_text": 'השתמש בפקודה /admin כדי להגדיר את שעת שליחת ההודעות ולניהול הודעות',
    "preferred_language": 'בחרת בשפה העברית, הפעל את הפקודה /profile כדי לבדוק',
    "change_language": 'בחר שפת תקשורת',
    "no_rights": '<b>שלום {0}!</b>\nלמרבה הצער, אין לך זכויות גישה לפקודה זו...\n<b>להתראות!</b>',
    "admin_panel": 'פאנל ניהול',
    "scheduler_manage": 'מתזמן...',
    "content_manage": 'ניהול תוכן...',
    "start_scheduler": 'התחל את מתזמן',
    "restart_scheduler": 'לחדש מתזמן',
    "stop_scheduler": 'עצור את מתזמן',
    "unknown_cmd": 'פקודה לא ידועה, בדוק את התחביר!',
    "select_content_type": 'בחר סוג תוכן',
    "openai": 'הפק באופן אוטומטי עם OpenAI',
    "external_csv": 'קובץ CSV חיצוני',
    "external_json": 'קובץ JSON חיצוני',
    "back_to_admin": 'חזור ללוח הניהול',
}


class MultiLang:
    def __init__(self, db: DataBase, lang: str = "en"):
        self.lang = lang
        self.db = db

    def get_lang(self):
        return self.lang

    def set_lang(self, lang):
        self.lang = lang

    def msg(self, msg_id, lang: str = ""):
        lang_selector = self.lang if lang == "" else lang
        if lang_selector == "ru":
            return MESSAGES_RU.get(msg_id)
        elif lang_selector == "en":
            return MESSAGES_EN.get(msg_id)
        else:
            return MESSAGES_HE.get(msg_id)
