from utils.db_api.create_db_tables import Database


class AdminDB:
    def __init__(self, db: Database):
        self.db = db

    # =========================== TABLE | SEND_STATUS ===========================
    async def add_send_status(self):
        sql = "INSERT INTO send_status (send_post) VALUES (false)"
        return await self.db.execute(sql, execute=True)

    async def update_send_status(self, send_post):
        sql = "UPDATE send_status SET send_post = $1"
        return await self.db.execute(sql, send_post, execute=True)

    async def get_send_status(self):
        sql = "SELECT send_post FROM send_status"
        return await self.db.execute(sql, fetchval=True)

    # =========================== DROP ROWS ===========================

    async def delete_from_yaxin(self):
        sql = """
            WITH deleted_rows AS (
                DELETE FROM temporaryyaxin 
                WHERE created_at < CURRENT_DATE 
                RETURNING id
            ) 
            SELECT COUNT(id) FROM deleted_rows
        """
        return await self.db.execute(sql, fetchval=True)

    async def delete_from_ayzenk(self):
        sql = """
            WITH deleted_rows AS (
                DELETE FROM ayztemptemp 
                WHERE created_at < CURRENT_DATE 
                RETURNING question_number
            ) 
            SELECT COUNT(question_number) FROM deleted_rows
        """
        return await self.db.execute(sql, fetchval=True)

    async def delete_from_leo(self):
        sql = """
            WITH deleted_rows AS (
                DELETE FROM leotemp 
                WHERE created_at < CURRENT_DATE 
                RETURNING question_number
            ) 
            SELECT COUNT(question_number) FROM deleted_rows
        """
        return await self.db.execute(sql, fetchval=True)
