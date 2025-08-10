from utils.db_api.create_db_tables import Database


class LeongardDB:
    def __init__(self, db: Database):
        self.db = db

    # ======================= TABLE | LEONGARD_QUESTIONS =======================
    async def add_leoquestions(self, question_number, question):
        sql = "INSERT INTO bot_leoquestions (question_number, question) VALUES ($1, $2)"
        return await self.db.execute(sql, question_number, question, fetchrow=True)

    async def select_questions_leo(self):
        sql = "SELECT * FROM bot_leoquestions ORDER BY question_number"
        return await self.db.execute(sql, fetch=True)

    # ======================= TABLE | LEONGARD_SCALES =======================
    async def add_leoscales(self, scale_type, yes, no_):
        sql = "INSERT INTO bot_leoscales (scale_type, yes, no_) VALUES ($1, $2, $3)"
        return await self.db.execute(sql, scale_type, yes, no_, fetchrow=True)

    async def get_yes_leoscales(self, yes):
        sql = f"SELECT scale_type FROM bot_leoscales WHERE yes={yes}"
        return await self.db.execute(sql, fetchrow=True)

    async def get_no_leoscales(self, no_):
        sql = f"SELECT scale_type FROM bot_leoscales WHERE no_='{no_}'"
        return await self.db.execute(sql, fetchrow=True)

    # ======================= TABLE | LEONGARD_TEMPORARY =======================
    async def add_leotemp(self, telegram_id, scale_type, question_number, yes=0, no_=0):
        sql = "INSERT INTO bot_leotemp (telegram_id, scale_type, question_number, yes, no_) VALUES ($1, $2, $3, $4, $5)"
        return await self.db.execute(sql, telegram_id, scale_type, question_number, yes, no_, fetchrow=True)

    async def select_check_leotemp(self, telegram_id, question_number):
        sql = f"SELECT * FROM bot_leotemp WHERE telegram_id=$1 AND question_number=$2"
        return await self.db.execute(sql, telegram_id, question_number, fetchrow=True)

    async def get_sums_leotemp(self, telegram_id, scale_type):
        sql = """
        SELECT scale_type, SUM(yes) AS total_yes, SUM(no_) AS total_no 
        FROM bot_leotemp 
        WHERE telegram_id=$1 AND scale_type=$2 
        GROUP BY scale_type
        """
        return await self.db.execute(sql, telegram_id, scale_type, fetchrow=True)

    async def delete_leotemp(self, telegram_id):
        await self.db.execute(f"DELETE FROM bot_leotemp WHERE telegram_id='{telegram_id}'", execute=True)

    async def back_leotemp(self, telegram_id, question_number):
        await self.db.execute(f"DELETE FROM bot_leotemp WHERE telegram_id='{telegram_id}' "
                              f"AND question_number='{question_number}'", execute=True)
