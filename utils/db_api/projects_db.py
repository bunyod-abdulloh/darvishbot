from utils.db_api.create_db_tables import Database


class ProjectsDB:
    def __init__(self, db: Database):
        self.db = db

    # =========================== TABLE | PROJECTS ===========================
    async def add_projects(self, sequence, file_id, file_type, category, subcategory, caption):
        sql = """
        INSERT INTO bot_medias (sequence, file_id, file_type, category, subcategory, caption) 
        VALUES ($1, $2, $3, $4, $5, $6) RETURNING *;
        """
        return await self.db.execute(sql, sequence, file_id, file_type, category, subcategory, caption, fetchrow=True)

    async def select_all_projects(self):
        sql = "SELECT * FROM bot_medias"
        return await self.db.execute(sql, fetch=True)

    async def select_projects(self):
        sql = """
        SELECT row_number() OVER () AS rank, category, id
        FROM (
            SELECT DISTINCT ON (category) category, id
            FROM bot_medias
            ORDER BY category, id ASC
        ) subquery
        """
        return await self.db.execute(sql, fetch=True)

    async def select_project_by_id(self, id_):
        sql = "SELECT * FROM bot_medias WHERE id=$1"
        return await self.db.execute(sql, id_, fetchrow=True)

    async def select_project_by_categories(self, category_name):
        sql = "SELECT * FROM bot_medias WHERE category=$1 ORDER BY sequence ASC"
        return await self.db.execute(sql, category_name, fetch=True)
