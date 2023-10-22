from datetime import datetime, timedelta

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from shared.config import Config
from database.sql import DataBase
from database.user_info import UserInfo


class ContentProvider:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.jobId = ""
        self.jobObj = 0
        self.scheduler = AsyncIOScheduler(timezone="Asia/Jerusalem")
        self.scheduler.start()

    def is_running(self):
        return bool(self.jobId)

    async def stop_scheduler(self):
        if self.jobId:
            self.scheduler.remove_job(self.jobId)
            self.jobId = ''
            return 'stopped'
        return 'not running'

    async def restart_scheduler(self):
        db: DataBase = self.bot.db
        sched = await db.get_scheduler()
        month = sched[0] if len(sched[0]) else None
        day = sched[1] if len(sched[1]) else None
        dow = sched[2] if len(sched[2]) else None
        hour = sched[3] if len(sched[3]) else None
        minute = sched[4] if len(sched[4]) else None
        jitter = int(sched[5]) if len(sched[5]) else None

        if self.jobId:
            self.scheduler.remove_job(self.jobId)
            self.jobId = ''

        self.jobId = str(id(datetime.now()))
        self.jobObj = self.scheduler.add_job(self.send_message, id=self.jobId, trigger='cron', month=month, day=day,
                                             day_of_week=dow, hour=hour, minute=minute, jitter=jitter,
                                             start_date=datetime.now())
        return self.jobObj.next_run_time

    async def send_message(self):
        print("send message")


