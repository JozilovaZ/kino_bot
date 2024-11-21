from .database import Database
from datetime import datetime


#UserDatabase foydalanuvchilarni bazaga saqlash uchun

class UserDatabase(Database):
    def create_table_users(self):
        sql = """
            CREATE TABLE IF NOT EXISTS Users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id BIGINT NOT NULL,
                username VARCHAR(255) NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                last_active DATETIME NULL
                );
                """
        self.execute(sql,commit=True)


    def add_user(self,telegram_id:int,username:str,created_at=None):
        sql="""
            INSERT INTO Users(telegram_id,username,created_at) VALUES(?,?,?)
            """
        if created_at is None:
            created_at=datetime.now().isoformat()

        self.execute(sql,parameters=(telegram_id,username,created_at),commit=True)

    def select_all_users(self):
        sql="""
            SELECT * FROM Users
            """
        self.execute(sql,fetchall=True)

    def count_users(self):
        sql = """
            SELECT COUNT(*) FROM Users
        """
        return self.execute(sql, fetchone=True)[0]


    def select_user(self, telegram_id: int):
        sql = """
            SELECT * FROM Users WHERE telegram_id = ?
        """
        return self.execute(sql, parameters=(telegram_id,), fetchone=True)





