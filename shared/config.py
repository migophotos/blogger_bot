from dataclasses import dataclass
import private.tokens as SECRET


@dataclass
class Config:
    bot_token: str = SECRET.CLIENT_BOT_TOKEN
    bot_name: str = "BloggerBot"
    db_path: str = './database/blogger_bot.db'
    admin_id: int = 565542529

    #  Russian channel
    smart_ch_ru_name: str = "БЗ Forever"
    smart_ch_ru_link: str = "@flp_rus_smart_channel"
    #   English channel
    smart_ch_en_name: str = "Eternal Wellness"
    smart_ch_en_link: str = "@flp_eng_smart_channel"
    #   Hebrew channel
    smart_ch_he_name: str = "חי לנצח"
    smart_ch_he_link: str = "@flp_heb_smart_channel"
    #                month, day, day of week, hour, minute, jitter (+- seconds)
    def_scheduler = ("", "*", "", "10", "", "")


