from utils.db_api.create_db_tables import Database


class UsersDB:
    def __init__(self, db: Database):
        self.db = db

    # =========================== TABLE | USERS ==========================
    async def add_user(self, telegram_id):
        sql = "INSERT INTO bot_users (telegram_id) VALUES($1) ON CONFLICT (telegram_id) DO NOTHING"
        return await self.db.execute(sql, telegram_id, execute=True)

    async def add_user_json(self, telegram_id, fio, phone):
        sql = "INSERT INTO bot_users (telegram_id, fio, phone) VALUES($1, $2, $3)"
        return await self.db.execute(sql, telegram_id, fio, phone, execute=True)

    async def update_user_info(self, telegram_id, age, gender):
        sql = """
        INSERT INTO bot_users (telegram_id, age, gender)
        VALUES ($1, $2, $3)
        ON CONFLICT (telegram_id)
        DO UPDATE SET age = EXCLUDED.age, gender = EXCLUDED.gender;
        """
        return await self.db.execute(sql, telegram_id, age, gender, execute=True)

    async def updateuser_fullname(self, telegram_id, fio):
        sql = f"UPDATE bot_users SET fio='{fio}' WHERE telegram_id='{telegram_id}'"
        return await self.db.execute(sql, execute=True)

    async def updateuser_phone(self, telegram_id, phone):
        sql = f"UPDATE bot_users SET phone='{phone}' WHERE telegram_id='{telegram_id}'"
        return await self.db.execute(sql, execute=True)

    async def select_all_users(self):
        sql = "SELECT * FROM bot_users"
        return await self.db.execute(sql, fetch=True)

    async def select_user(self, telegram_id):
        sql = f"SELECT * FROM bot_users WHERE telegram_id='{telegram_id}'"
        return await self.db.execute(sql, fetchrow=True)

    async def check_user(self, telegram_id):
        sql = f"""
            SELECT EXISTS (
                SELECT 1 FROM bot_users 
                WHERE telegram_id = $1 
                AND gender IS NOT NULL 
                AND age IS NOT NULL
            )
        """
        return await self.db.execute(sql, telegram_id, fetchval=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM bot_users"
        return await self.db.execute(sql, fetchval=True)

    async def delete_user(self, telegram_id):
        await self.db.execute(f"DELETE FROM bot_users WHERE telegram_id='{telegram_id}'", execute=True)

    async def drop_table_users(self):
        await self.db.execute("DROP TABLE bot_users", execute=True)
