from utils.db_api.create_db_tables import Database


class YaxinDB:
    def __init__(self, db: Database):
        self.db = db

    # =================== TESTLAR | YAXIN ========================
    async def add_questions_yaxin(self, scale_type, question, a, b, c, d, e):
        sql = """
        INSERT INTO bot_tt_yaxin (scale_type, question, a, b, c, d, e) 
        VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING *;
        """
        return await self.db.execute(sql, scale_type, question, a, b, c, d, e, fetchrow=True)

    async def select_all_yaxin(self):
        sql = "SELECT * FROM bot_tt_yaxin ORDER BY id"
        return await self.db.execute(sql, fetch=True)

    # ======================= TABLE | YAXIN_SCALES =======================
    async def add_yaxin_scales(self, scale_type, question_number, point_one, point_two, point_three, point_four,
                               point_five):
        sql = """
        INSERT INTO bot_yaxinscales (scale_type, question_number, point_one, point_two, point_three, point_four, point_five) 
        VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING *;
        """
        return await self.db.execute(sql, scale_type, question_number, point_one, point_two, point_three, point_four,
                                  point_five, fetchrow=True)

    async def select_question_scale(self, scale_type, question_number):
        sql = "SELECT * FROM bot_yaxinscales WHERE scale_type=$1 AND question_number=$2"
        return await self.db.execute(sql, scale_type, question_number, fetchrow=True)

    # ======================= TABLE | YAXIN_TEMPORARY =======================
    async def add_yaxin_temporary(self, telegram_id, test_type, scale_type, question_number, answer):
        sql = """
        INSERT INTO bot_tempyaxin (telegram_id, test_type, scale_type, question_number, answer) 
        VALUES ($1, $2, $3, $4, $5) RETURNING *;
        """
        return await self.db.execute(sql, telegram_id, test_type, scale_type, question_number, answer, fetchrow=True)

    async def select_datas_temporary(self, telegram_id, scale_type):
        sql = """
        SELECT ROUND(SUM(answer), 2) 
        FROM bot_tempyaxin 
        WHERE telegram_id=$1 AND scale_type=$2;
        """
        return await self.db.execute(sql, telegram_id, scale_type, fetchval=True)

    async def delete_user_yaxintemporary(self, telegram_id):
        sql = "DELETE FROM bot_tempyaxin WHERE telegram_id=$1"
        await self.db.execute(sql, telegram_id, execute=True)

    async def back_yaxintemporary(self, telegram_id, question_number):
        sql = "DELETE FROM bot_tempyaxin WHERE telegram_id=$1 AND question_number=$2"
        await self.db.execute(sql, telegram_id, question_number, execute=True)

    # ======================= TABLE | YAXIN_ANSWERS =======================
    async def add_yaxinanswers(self, full_name, telegram_id, test_type, scale_type, all_points):
        sql = """
        INSERT INTO bot_yaxinanswers (full_name, telegram_id, test_type, scale_type, all_points) 
        VALUES ($1, $2, $3, $4, $5) RETURNING *;
        """
        return await self.db.execute(sql, full_name, telegram_id, test_type, scale_type, all_points, fetchrow=True)

    async def delete_user_yaxinanswers(self, telegram_id):
        sql = "DELETE FROM bot_yaxinanswers WHERE telegram_id=$1"
        await self.db.execute(sql, telegram_id, execute=True)
