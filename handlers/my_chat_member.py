from aiogram import F, Router, Bot
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.filters.command import CommandStart, Command
from aiogram.types import ChatMemberUpdated

from database.sql import DataBase

router = Router()
router.my_chat_member.filter(F.chat.type == "private")
router.message.filter(F.chat.type == "private")


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated, bot: Bot):
    db: DataBase = event.bot.db
    await db.delete_user(event.from_user.id)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated, bot: Bot):
    db: DataBase = bot.db
    await db.add_user(event.from_user.id, event.from_user.first_name, event.from_user.language_code)
