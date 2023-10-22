from aiogram import Bot, Router
from aiogram.types import Message, CallbackQuery

from database.sql import DataBase
from database.user_info import UserInfo
from handlers.callback_factory import SchedulerCbFactory

router = Router()


async def show_cur_scheduler(msg: Message, from_cb=True):
    if msg.bot.db:
        sched = await msg.bot.db.get_scheduler()
        month = sched[0]
        day = sched[1]
        dow = sched[2]
        hour = sched[3]
        minute = sched[4]
        jitter = sched[5]
        month_str = '' if month == "" else f'Month: {month}\n'
        day_str = '' if day == "" else f'Day: {day}\n'
        dow_str = '' if dow == "" else f'Day of Week: {dow}\n'
        hour_str = '' if hour == "" else f'Hour: {hour}\n'
        minute_str = '' if minute == "" else f'Minute: {minute}\n'
        jitter_str = '' if jitter == "" else f'Jitter: {jitter}\n'

        # if month == "*" or month == "":
        #     month_str = "Каждый месяц"
        sched_str = f"<b>Current Scheduler:</b>\n" \
                    f"{month_str}{day_str}{dow_str}{hour_str}{minute_str}{jitter_str}" \
                    f"\n<b>Possible keys:</b>\n" \
                    f"mth: - month (1-12)\n" \
                    f"d: - day (1-31) \n" \
                    f"dow: -day of week (0-6)\n" \
                    f"h: - hour (0-23)\n" \
                    f"m: - minute (0-59)\n" \
                    f"j: - jitter (1-60)\n" \
                    f"<b>Values:</b>\n" \
                    f"* - each day, month, day of week, hour and minute\n" \
                    f"/N - every N, for ex: h:*/2 - every two hours\n" \
                    f", - enumeration of values, for ex: dof:1,3,5 - first, third and fifth day of week\n" \
                    f"\n<b><u>Examples of use</u></b>:\n" \
                    f"Runs every minute at 17 o'clock\n" \
                    f"<b>h:17 m:*</b>\n" \
                    f"Runs every 2 minutes\n" \
                    f"<b>m:*/2</b>\n" \
                    f"Runs once a day at 17:30 and 18:30\n" \
                    f"<b>h:17-18 m:30</b>\n" \
                    f"Runs each day exclude Sat at 10 o'clock, but with an extra delay of -60 to +60 seconds\n" \
                    f"<b>dow:0-6 h:10 m:30 j:60</b>\n" \
                    f"Runs on the months June, July, August each day at 9:00, 10:00 and 11:00\n" \
                    f"<b>mth:6-8 d:* h:9-11</b>\n\n" \
                    f"Enter scheduler parameters starting with <b>'cmd:sc '</b> or <b>'exit:sc'</b> to EXIT"
        if from_cb:
            await msg.edit_text(sched_str)
        else:
            await msg.answer(sched_str)


@router.callback_query(SchedulerCbFactory.filter())
async def scheduler_manage(call: CallbackQuery, callback_data: SchedulerCbFactory, bot: Bot):
    db: DataBase = bot.db
    ui = UserInfo(db)
    await ui.init_user_info(call.message)  # init user info
    bot.ml.set_lang(ui.get_language())

    await show_cur_scheduler(call.message)
    await call.answer()


async def set_new_scheduler(text: str, msg: Message):
    #                month, day, day of week, hour, minute, jitter (+- seconds)
    # def_scheduler = ("", "*", "", "10", "", "")

    month = day = day_of_week = hour = minute = jitter = ""

    params = text.split(' ')
    if len(params) > 1 and params[0].lower() == 'cmd:sc':
        for index in range(1, len(params)):
            param = params[index]
            if param.startswith('mth:'):
                month = param.replace('mth:', '')
            if param.startswith('d:'):
                day = param.replace('d:', '')
            if param.startswith('dow:'):
                day_of_week = param.replace('dow:', '')
            if param.startswith('h:'):
                hour = param.replace('h:', '')
            if param.startswith('m:'):
                minute = param.replace('m:', '')
            if param.startswith('j:'):
                jitter = param.replace('j:', '')

        new_scheduler = (month, day, day_of_week, hour, minute, jitter)
        db: DataBase = msg.bot.db
        if db:
            await db.update_scheduler(new_scheduler)
            await show_cur_scheduler(msg, from_cb=False)

