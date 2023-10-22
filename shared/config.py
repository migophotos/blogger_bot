from dataclasses import dataclass
import private.tokens as SECRET


@dataclass
class Config:
    bot_token: str = SECRET.CLIENT_BOT_TOKEN
    bot_name: str = "BloggerBot"
    db_path: str = './database/blogger_bot.db'
    admin_id: int = 565542529

    #  Russian channel
    channel_ru_name: str = "БЗ Forever"
    channel_ru_link: str = "@flp_rus_smart_channel"
    #   English channel
    channel_en_name: str = "Eternal Wellness"
    channel_en_link: str = "@flp_eng_smart_channel"
    #   Hebrew channel
    channel_he_name: str = "חי לנצח"
    channel_he_link: str = "@flp_heb_smart_channel"
    #                month, day, day of week, hour, minute, jitter (+- seconds)
    def_scheduler = ("", "*", "", "10", "", "")


