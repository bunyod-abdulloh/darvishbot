from utils.db_api.create_db_tables import Database


class StatisticsDB:
    def __init__(self, db: Database):
        self.db = db

    async def add_to_statistics(self, telegram_id: int, age: int, gender: str):
        sql = """
        INSERT INTO bot_statistics (user_id, age, gender)
        SELECT id, $2, $3 FROM bot_users WHERE telegram_id = $1
        ON CONFLICT (user_id) DO NOTHING
        """
        return await self.db.execute(sql, telegram_id, age, gender, execute=True)

    async def check_user_in_statistics(self, telegram_id):
        sql = """
            SELECT EXISTS (
                SELECT 1
                FROM bot_statistics s
                JOIN bot_users u ON s.user_id = u.id
                WHERE u.telegram_id = $1
            )
        """
        return await self.db.execute(sql, telegram_id, fetchval=True)

    async def set_test_result(self, telegram_id, test_type, result):
        sql = """
        INSERT INTO bot_statistics (user_id, test_type, result, created_at)
        SELECT id, $2, $3, CURRENT_DATE FROM bot_users WHERE telegram_id = $1
        ON CONFLICT (user_id, test_type)
        DO UPDATE SET 
            result = EXCLUDED.result,
            created_at = CURRENT_DATE;
        """
        return await self.db.execute(sql, telegram_id, test_type, result, execute=True)
