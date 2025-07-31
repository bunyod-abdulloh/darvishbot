from utils.db_api.create_db_tables import Database


class ArticlesDB:
    def __init__(self, db: Database):
        self.db = db

    # =========================== TABLE | ARTICLES ===========================
    async def add_articles(self, file_name, link):
        sql = "INSERT INTO bot_articles (file_name, link) VALUES($1, $2) RETURNING *"
        return await self.execute(sql, file_name, link, fetchrow=True)

    async def select_all_articles(self):
        sql = "SELECT * FROM bot_articles ORDER BY id"
        return await self.execute(sql, fetch=True)
