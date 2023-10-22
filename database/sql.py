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
        await self.create_content()

    async def create_users(self):
        try:
            with self.connect:
                self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                userid INT PRIMARY KEY,
                fname TEXT,
                lang TEXT,
                role TEXT,
                content_type TEXT);
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

    async def create_content(self):
        """
        content_type: "openai", "custom"
        subject: any subject theme, that describes the generated content, for ex: "news", "sport", "technology",...
        ru_prompt: prompt for generation text on russian language, if empty, no text will be generated
        en_prompt: prompt for generation text on english language, if empty, no text will be generated
        he_prompt: prompt for generation text on hebrew language, if empty, no text will be generated
        title: title of publication
        body: body of publication
        images: comma-separated list of images
        :return:
        """
        try:
            with self.connect:
                self.cursor.execute("""CREATE TABLE IF NOT EXISTS content(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_type TEXT,
                subject TEXT,
                ru_prompt TEXT,
                en_prompt TEXT,
                he_prompt TEXT,
                title TEXT,
                body TEXT,
                images TEXT);
                """)
                self.connect.commit()
        except sqlite3.Error as er:
            print("Failed to create table: 'content'", er)

    async def update_data(self, table, param, id, value):
        try:
            data = (value, id)
            sql_str = f"UPDATE {table} SET {param}=(?) WHERE id=(?)"
            self.cursor.execute(sql_str, data)
            self.connect.commit()
        except sqlite3.Error as error:
            print("Failed to update", error)

    async def get_content(self, content_type):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM content WHERE content_type=(?)""", [content_type]).fetchall()

    async def delete_content(self, id):
        with self.connect:
            return self.cursor.execute("""DELETE FROM content WHERE id IN (?)""", [id]).fetchall()

    async def add_content(self, content: tuple):
        try:
            with self.connect:
                return self.cursor.execute("INSERT INTO content VALUES(?, ?, ?, ?, ?, ?, ?, ?);", content)
        except sqlite3.Error as error:
            print("Failed to add content", error)

    async def add_user(self, user_id, first_name, lang, role="guest", content_type="none"):
        try:
            with self.connect:
                return self.cursor.execute(
                    """INSERT INTO users (userid, fname, lang, role, content_type)  VALUES (?, ?, ?, ?, ?)""",
                    [user_id,
                     first_name,
                     lang,
                     'admin' if user_id == Config.admin_id else role,
                     content_type])
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
