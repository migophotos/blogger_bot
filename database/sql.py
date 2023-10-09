from shared.config import Config
import sqlite3


class DataBase:
    def __init__(self, db_file):
        self.connect = sqlite3.connect(db_file)
        self.cursor = self.connect.cursor()

    async def disconnect(self):
        self.cursor.close()
        self.connect.close()

    async def create_tables(self):
        await self.create_users()
        await self.create_scheduler()

    async def create_users(self):
        try:
            with self.connect:
                self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                userid INT PRIMARY KEY,
                fname TEXT,
                lang TEXT,
                role TEXT);
                """)
                self.connect.commit()
        except sqlite3.Error as er:
            print("Failed to create table: 'users'", er)

    async def create_scheduler(self):
        try:
            with self.connect:
                self.cursor.execute("""CREATE TABLE IF NOT EXISTS scheduler(
                month TEXT,
                day TEXT,
                day_of_week TEXT,
                hour TEXT,
                minute TEXT,
                jitter TEXT);
                """)
                self.connect.commit()
        except sqlite3.Error as er:
            print("Failed to create table: 'scheduler'", er)

    async def add_user(self, user_id, first_name, lang, role="guest"):
        try:
            with self.connect:
                return self.cursor.execute(
                    """INSERT INTO users (userid, fname, lang, role)  VALUES (?, ?, ?, ?)""",
                    [user_id,
                     first_name,
                     lang,
                     'admin' if user_id == Config.admin_id else role])
        except sqlite3.Error as error:
            print("Failed to add new user", error)

    async def get_users(self):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM users""").fetchall()

    async def get_user(self, user_id):
        with self.connect:
            user = self.cursor.execute("SELECT * FROM users WHERE userid=(?);", [user_id]).fetchone()
            if user and len(user) > 0:
                return user
            # user with specified id not found, return empty array
            return []

    async def update_user(self, user_id, param, value):
        try:
            data = (value, user_id)
            sql_str = f"UPDATE users SET {param}=(?) WHERE userid=(?)"
            self.cursor.execute(sql_str, data)
            self.connect.commit()
        except sqlite3.Error as error:
            print("Failed to update", error)

    async def delete_user(self, id):
        with self.connect:
            return self.cursor.execute("""DELETE FROM users WHERE userid IN (?)""", [id]).fetchall()

    async def get_scheduler(self):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM scheduler""").fetchone()

    async def insert_def_scheduler(self):
        with self.connect:
            if not self.cursor.execute("""SELECT * FROM scheduler""").fetchone():
                self.cursor.execute("""INSERT INTO scheduler VALUES(?, ?, ?, ?, ?, ?)""", Config.def_scheduler)

    async def update_scheduler(self, params):
        with self.connect:
            self.cursor.execute('''UPDATE scheduler SET month=(?), day=(?), day_of_week=(?), hour=(?), minute=(?), jitter=(?)''', params)

