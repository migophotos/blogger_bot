from database.user_info import UserInfo
from shared.messages import MultiLang
from shared.config import Config


def logger(function):
    def wrapper(*args, **kwargs):
        print(f"----- {function.__name__}: start -----")
        output = function(*args, **kwargs)
        print(f"----- {function.__name__}: end -----")
        return output
    return wrapper


def build_profile_text(ui: UserInfo, ml: MultiLang):
    profile_text = f'{ml.msg("hello")} <b>{ui.get_first_name()}</b>' \
                   f'\n<b>{ml.msg("your_role")}</b>: {ui.get_role()}' \
                   f'\n<b>{ml.msg("your_id")}</b>: {ui.get_id()}' \
                   f'\n<b>{ml.msg("your_lang")}</b>: {ui.get_language()}'

    return profile_text


def build_start_message(ui: UserInfo, ml: MultiLang):
    admin_text = ''
    if ui.is_admin():
        admin_text += ml.msg("admin_text")

    channels = ""
    for channel in Config.channels_list:
        channels += f'<b>{Config.channels_list[channel][0]}</b>: <u>{Config.channels_list[channel][1]}</u>\n'

    start_message = f'{ml.msg("about_bot")}\n\n' \
                    f'{admin_text}\n\n' \
                    f'{ml.msg("channel_invitation").format(channels)}',

    return start_message[0]


def build_help_message(ui: UserInfo, ml: MultiLang):
    return build_start_message(ui, ml)