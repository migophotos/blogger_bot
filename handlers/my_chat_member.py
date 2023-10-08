from aiogram import F, Router, Bot
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.filters.command import CommandStart, Command
from aiogram.types import ChatMemberUpdated, Message

from database.sql import DataBase

router = Router()
router.my_chat_member.filter(F.chat.type == "private")
router.message.filter(F.chat.type == "private")


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated, bot: Bot):
    # users.discard(event.from_user.id)
    db: DataBase = bot.db


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated, bot: Bot):
    # users.add(event.from_user.id)
    db: DataBase = bot.db
