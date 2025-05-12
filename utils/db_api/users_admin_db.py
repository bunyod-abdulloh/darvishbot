from utils.db_api.postgres import Database


class UsersDB:
    def __init__(self, db: Database):
        self.db = db

    # =========================== TABLE | USERS ==========================
    async def add_user(self, telegram_id):
        sql = "INSERT INTO users (telegram_id) VALUES($1)"
        return await self.db.execute(sql, telegram_id, execute=True)

    async def add_user_json(self, telegram_id, fio, phone):
        sql = "INSERT INTO users (telegram_id, fio, phone) VALUES($1, $2, $3)"
        return await self.db.execute(sql, telegram_id, fio, phone, execute=True)

    async def updateuser_fullname(self, telegram_id, fio):
        sql = f"UPDATE users SET fio='{fio}' WHERE telegram_id='{telegram_id}'"
        return await self.db.execute(sql, execute=True)

    async def updateuser_phone(self, telegram_id, phone):
        sql = f"UPDATE users SET phone='{phone}' WHERE telegram_id='{telegram_id}'"
        return await self.db.execute(sql, execute=True)

    async def select_all_users(self):
        sql = "SELECT * FROM users"
        return await self.db.execute(sql, fetch=True)

    async def select_user(self, telegram_id):
        sql = f"SELECT * FROM users WHERE telegram_id='{telegram_id}'"
        return await self.db.execute(sql, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM users"
        return await self.db.execute(sql, fetchval=True)

    async def delete_user(self, telegram_id):
        await self.db.execute(f"DELETE FROM users WHERE telegram_id='{telegram_id}'", execute=True)

    async def drop_table_users(self):
        await self.db.execute("DROP TABLE users", execute=True)
