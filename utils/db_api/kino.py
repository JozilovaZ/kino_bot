from .database import Database
from datetime import datetime


#Kinolarni saqlash uchun database classi
class KinoDatabase(Database):
    def create_table_kino(self):
       sql = """
                CREATE TABLE IF NOT EXISTS Kino(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id BIGINT  NOT NULL UNIQUE,
                    file_id VARCHAR(2000) NOT NULL,
                    caption TEXT NULL,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    count_download INTEGER NOT NULL DEFAULT 0,
                    updated_at DATETIME
                    );
            """
       self.execute(sql,commit=True)

    def add_kino(self,post_id:int,file_id:str,caption:str):
        sql="""
            INSERT INTO Kino(post_id,file_id,caption,created_at,updated_at) VALUES(?,?,?,?,?)
            """
        timestamp=datetime.now().isoformat()
        self.execute(sql,parameters=(post_id,file_id,caption,timestamp,timestamp),commit=True)

    def delete_kino(self,post_id):
        sql="""
            DELETE FROM Kino WHERE post_id=?
            """
        self.execute(sql,parameters=(post_id,),commit=True)


    def search_kino_by_post_id(self,post_id):
        sql="""
            SELECT file_id,caption FROM Kino WHERE post_id=?
            """

        result=self.execute(sql,parameters=(post_id,),fetchone=True)
        return {"file_id":result[0],"caption":result[1] if result else None}


    def count_kinos(self):
        sql="""
            SELECT COUNT(*) FROM Kino
            """
        result=self.execute(sql,fetchone=True)
        return {"count":result[0] if result else None}


