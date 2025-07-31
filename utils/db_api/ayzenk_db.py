from utils.db_api.create_db_tables import Database


class AyzenkDB:
    def __init__(self, db: Database):
        self.db = db

    # ======================= TABLE | AYZENK_TEMPERAMENT =======================
    async def add_ayztempquestion(self, question_number, question):
        sql = "INSERT INTO bot_ayztempquestions (question_number, question) VALUES ($1, $2)"
        return await self.db.execute(sql, question_number, question, fetchrow=True)

    async def select_questions_ayztemp(self):
        sql = "SELECT * FROM bot_ayztempquestions ORDER BY question_number"
        return await self.db.execute(sql, fetch=True)

    # ======================= TABLE | AYZENK_SCALES =======================
    async def add_ayztempscales(self, scale_type, yes, no_):
        sql = "INSERT INTO bot_ayztempscales (scale_type, yes, no_) VALUES ($1, $2, $3)"
        return await self.db.execute(sql, scale_type, yes, no_, fetchrow=True)

    async def get_ayzscales_by_value(self, value, column):
        sql = f"SELECT scale_type FROM bot_ayztempscales WHERE {column}=$1"
        return await self.db.execute(sql, value, fetchrow=True)

    # ======================= TABLE | AYZENK_TEMP =======================
    async def add_ayztemptempyes(self, telegram_id, scale_type, question_number, yes):
        sql = "INSERT INTO bot_ayztemptemp (telegram_id, scale_type, question_number, yes) VALUES ($1, $2, $3, $4)"
        return await self.db.execute(sql, telegram_id, scale_type, question_number, yes, fetchrow=True)

    async def add_ayztemptempno(self, telegram_id, scale_type, question_number, no_):
        sql = "INSERT INTO bot_ayztemptemp (telegram_id, scale_type, question_number, no_) VALUES ($1, $2, $3, $4)"
        return await self.db.execute(sql, telegram_id, scale_type, question_number, no_, fetchrow=True)

    async def select_sum_ayztemptemp(self, telegram_id, scale_type, column):
        sql = f"SELECT SUM({column}) FROM bot_ayztemptemp WHERE telegram_id=$1 AND scale_type=$2"
        return await self.db.execute(sql, telegram_id, scale_type, fetchrow=True)

    async def select_check_ayztemptemp(self, telegram_id, question_number):
        sql = f"SELECT * FROM bot_ayztemptemp WHERE telegram_id=$1 AND question_number=$2"
        return await self.db.execute(sql, telegram_id, question_number, fetchrow=True)

    async def back_user_ayztemptemp(self, telegram_id, question_number):
        await self.db.execute(f"DELETE FROM bot_ayztemptemp WHERE telegram_id='{telegram_id}' "
                           f"AND question_number='{question_number}'", execute=True)

    async def delete_ayztemptemp(self, telegram_id):
        await self.db.execute(f"DELETE FROM bot_ayztemptemp WHERE telegram_id='{telegram_id}'", execute=True)

