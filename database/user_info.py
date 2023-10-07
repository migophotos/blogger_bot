from aiogram.types import Message
from database.sql import DataBase


class UserInfo:
    def __init__(self, database: DataBase):
        self.db = database
        self.user_data = {}

    async def init_user_info(self, message: Message):
        u_id = message.from_user.id
        u_name = message.from_user.first_name
        u_lang = message.from_user.language_code
        if message.from_user.is_bot is True:
            u_id = message.chat.id
            u_name = message.chat.first_name
            u_lang = 'en'

        user = await self.db.get_user(u_id)
        if len(user) == 0:
            await self.db.add_user(u_id, u_name, u_lang, 'guest')

        await self.set_user(u_id)
        return self

    async def set_user(self, user_id):
        user = await self.db.get_user(user_id)
        if len(user) == 4:
            self.user_data["user_id"] = user[0]
            self.user_data["first_name"] = user[1]
            self.user_data["lang"] = user[2]
            self.user_data["role"] = user[3]

    def get_id(self):
        return self.user_data["user_id"]

    def get_role(self):
        return self.user_data["role"]

    def get_first_name(self):
        return self.user_data["first_name"]

    def get_language(self):
        return self.user_data["lang"]

    async def update_user_info(self, param, value):
        await self.db.update_user(self.get_id(), param, value)
        self.user_data[param] = value

    def is_valid_user(self):
        if self.user_data.get("user_id") is not None:
            return True
        return False

    def is_admin(self):
        if self.is_valid_user() and self.user_data["role"] == "admin":
            return True

        return False

