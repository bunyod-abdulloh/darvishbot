from typing import Union

import asyncpg
from asyncpg import Connection, Pool
from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        """Create the connection pool for database."""
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(self, command, *args, fetch=False, fetchval=False, fetchrow=False, execute=False):
        """Execute database commands."""
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    return await connection.fetch(command, *args)
                elif fetchval:
                    return await connection.fetchval(command, *args)
                elif fetchrow:
                    return await connection.fetchrow(command, *args)
                elif execute:
                    return await connection.execute(command, *args)

    async def create_tables(self):
        """Create the required tables in the database."""
        queries = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,                
                telegram_id BIGINT NOT NULL UNIQUE,
                fio VARCHAR(255) NULL,
                phone VARCHAR(30) NULL                
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS send_status (
                id SERIAL PRIMARY KEY,
                send_post BOOLEAN DEFAULT FALSE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS articles (
                id SERIAL PRIMARY KEY NOT NULL,
                file_name VARCHAR(150) NULL,
                link VARCHAR(150) NULL        
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS medialar_table9 (
                id SERIAL PRIMARY KEY NOT NULL,
                sequence INTEGER NOT NULL,
                file_id VARCHAR(200) NULL,
                file_type VARCHAR(20) NULL,
                category VARCHAR(50) NOT NULL,
                subcategory VARCHAR(50) NOT NULL,
                caption TEXT NULL,
                link VARCHAR(200) NULL        
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS testlar_nevrozyaxin(
                id SERIAL PRIMARY KEY,
                scale_type VARCHAR(50) NOT NULL,
                question TEXT NOT NULL,
                a VARCHAR(50) NOT NULL,
                b VARCHAR(50) NOT NULL,
                c VARCHAR(50) NOT NULL,
                d VARCHAR(50) NOT NULL,
                e VARCHAR(50) NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS yaxinscales (
                scale_type VARCHAR (50) NOT NULL,
                question_number INTEGER NULL,
                point_one FLOAT NULL,
                point_two FLOAT NULL,
                point_three FLOAT NULL,
                point_four FLOAT NULL,
                point_five FLOAT NULL        
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS temporaryyaxin (
                id SERIAL PRIMARY KEY,
                created_at DATE DEFAULT CURRENT_DATE,        
                fullname VARCHAR(255) NULL,
                phone VARCHAR(30) NULL,
                telegram_id BIGINT NOT NULL,
                test_type VARCHAR(50) NOT NULL,
                scale_type VARCHAR(50) NULL,
                question_number INTEGER NULL,
                answer NUMERIC NULL                
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS yaxinanswers (
                id SERIAL PRIMARY KEY,
                date_created DATE DEFAULT CURRENT_DATE,
                full_name VARCHAR(255) NOT NULL,
                telegram_id BIGINT NOT NULL,
                test_type VARCHAR(50) NOT NULL,
                scale_type VARCHAR(50) NULL,
                all_points NUMERIC NULL                        
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS ayztempquestions (
                id SERIAL PRIMARY KEY,                  
                question_number INTEGER NOT NULL,           
                question TEXT NOT NULL                                    
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS ayztempscales (  
                id SERIAL PRIMARY KEY,              
                scale_type VARCHAR(50) NOT NULL,       
                yes INTEGER NOT NULL,           
                no_ INTEGER NOT NULL                                    
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS ayztemptemp (
                created_at DATE DEFAULT CURRENT_DATE,  
                telegram_id BIGINT NOT NULL,              
                scale_type VARCHAR(50) NULL,
                question_number INTEGER NULL,       
                yes INTEGER NULL,           
                no_ INTEGER NULL                                    
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS leoquestions (                          
                question_number INTEGER NOT NULL,                   
                question TEXT NOT NULL                                            
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS leoscales (                          
                id SERIAL PRIMARY KEY,
                scale_type VARCHAR(15) NOT NULL,        
                yes INTEGER NULL,
                no_ INTEGER NULL                                    
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS leotemp (
                created_at DATE DEFAULT CURRENT_DATE,  
                telegram_id BIGINT NOT NULL,              
                scale_type VARCHAR(50) NULL,
                question_number INTEGER NULL,       
                yes INTEGER DEFAULT 0,            
                no_ INTEGER DEFAULT 0                                                    
            );
            """
        ]
        # Execute each table creation query
        for query in queries:
            await self.execute(query, execute=True)

    # =========================== TABLE | ARTICLES ===========================
    async def add_articles(self, file_name, link):
        sql = "INSERT INTO articles (file_name, link) VALUES($1, $2) RETURNING *"
        return await self.execute(sql, file_name, link, fetchrow=True)

    async def select_all_articles(self):
        sql = "SELECT * FROM articles ORDER BY id"
        return await self.execute(sql, fetch=True)

    # =========================== TABLE | PROJECTS ===========================
    async def add_projects(self, sequence, file_id, file_type, category, subcategory, caption):
        sql = """
        INSERT INTO medialar_table9 (sequence, file_id, file_type, category, subcategory, caption) 
        VALUES ($1, $2, $3, $4, $5, $6) RETURNING *;
        """
        return await self.execute(sql, sequence, file_id, file_type, category, subcategory, caption, fetchrow=True)

    async def select_all_projects(self):
        sql = "SELECT * FROM medialar_table9"
        return await self.execute(sql, fetch=True)

    async def select_projects(self):
        sql = """
        SELECT row_number() OVER () AS rank, category, id
        FROM (
            SELECT DISTINCT ON (category) category, id
            FROM medialar_table9
            ORDER BY category, id ASC
        ) subquery
        """
        return await self.execute(sql, fetch=True)

    async def select_project_by_id(self, id_):
        sql = "SELECT * FROM medialar_table9 WHERE id=$1"
        return await self.execute(sql, id_, fetchrow=True)

    async def select_project_by_categories(self, category_name):
        sql = "SELECT * FROM medialar_table9 WHERE category=$1 ORDER BY sequence ASC"
        return await self.execute(sql, category_name, fetch=True)

    # =================== TESTLAR | YAXIN ========================

    async def add_questions_yaxin(self, scale_type, question, a, b, c, d, e):
        sql = """
        INSERT INTO testlar_nevrozyaxin (scale_type, question, a, b, c, d, e) 
        VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING *;
        """
        return await self.execute(sql, scale_type, question, a, b, c, d, e, fetchrow=True)

    async def select_all_yaxin(self):
        sql = "SELECT * FROM testlar_nevrozyaxin ORDER BY id"
        return await self.execute(sql, fetch=True)

    # ======================= TABLE | YAXIN_SCALES =======================
    async def add_yaxin_scales(self, scale_type, question_number, point_one, point_two, point_three, point_four,
                               point_five):
        sql = """
        INSERT INTO yaxinscales (scale_type, question_number, point_one, point_two, point_three, point_four, point_five) 
        VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING *;
        """
        return await self.execute(sql, scale_type, question_number, point_one, point_two, point_three, point_four,
                                  point_five, fetchrow=True)

    async def select_question_scale(self, scale_type, question_number):
        sql = "SELECT * FROM yaxinscales WHERE scale_type=$1 AND question_number=$2"
        return await self.execute(sql, scale_type, question_number, fetchrow=True)

    # ======================= TABLE | YAXIN_TEMPORARY =======================
    async def add_yaxin_temporary(self, telegram_id, test_type, scale_type, question_number, answer):
        sql = """
        INSERT INTO temporaryyaxin (telegram_id, test_type, scale_type, question_number, answer) 
        VALUES ($1, $2, $3, $4, $5) RETURNING *;
        """
        return await self.execute(sql, telegram_id, test_type, scale_type, question_number, answer, fetchrow=True)

    async def select_datas_temporary(self, telegram_id, scale_type):
        sql = """
        SELECT ROUND(SUM(answer), 2) 
        FROM temporaryyaxin 
        WHERE telegram_id=$1 AND scale_type=$2;
        """
        return await self.execute(sql, telegram_id, scale_type, fetchval=True)

    async def delete_user_yaxintemporary(self, telegram_id):
        sql = "DELETE FROM temporaryyaxin WHERE telegram_id=$1"
        await self.execute(sql, telegram_id, execute=True)

    async def back_yaxintemporary(self, telegram_id, question_number):
        sql = "DELETE FROM temporaryyaxin WHERE telegram_id=$1 AND question_number=$2"
        await self.execute(sql, telegram_id, question_number, execute=True)

    # ======================= TABLE | YAXIN_ANSWERS =======================
    async def add_yaxinanswers(self, full_name, telegram_id, test_type, scale_type, all_points):
        sql = """
        INSERT INTO yaxinanswers (full_name, telegram_id, test_type, scale_type, all_points) 
        VALUES ($1, $2, $3, $4, $5) RETURNING *;
        """
        return await self.execute(sql, full_name, telegram_id, test_type, scale_type, all_points, fetchrow=True)

    async def delete_user_yaxinanswers(self, telegram_id):
        sql = "DELETE FROM yaxinanswers WHERE telegram_id=$1"
        await self.execute(sql, telegram_id, execute=True)

    # ======================= TABLE | AYZENK_TEMPERAMENT =======================
    async def add_ayztempquestion(self, question_number, question):
        sql = "INSERT INTO ayztempquestions (question_number, question) VALUES ($1, $2)"
        return await self.execute(sql, question_number, question, fetchrow=True)

    async def select_questions_ayztemp(self):
        sql = "SELECT * FROM ayztempquestions ORDER BY question_number"
        return await self.execute(sql, fetch=True)

    # ======================= TABLE | AYZENK_SCALES =======================
    async def add_ayztempscales(self, scale_type, yes, no_):
        sql = "INSERT INTO ayztempscales (scale_type, yes, no_) VALUES ($1, $2, $3)"
        return await self.execute(sql, scale_type, yes, no_, fetchrow=True)

    async def get_ayzscales_by_value(self, value, column):
        sql = f"SELECT scale_type FROM ayztempscales WHERE {column}=$1"
        return await self.execute(sql, value, fetchrow=True)

    # ======================= TABLE | AYZENK_TEMP =======================
    async def add_ayztemptempyes(self, telegram_id, scale_type, question_number, yes):
        sql = "INSERT INTO ayztemptemp (telegram_id, scale_type, question_number, yes) VALUES ($1, $2, $3, $4)"
        return await self.execute(sql, telegram_id, scale_type, question_number, yes, fetchrow=True)

    async def add_ayztemptempno(self, telegram_id, scale_type, question_number, no_):
        sql = "INSERT INTO ayztemptemp (telegram_id, scale_type, question_number, no_) VALUES ($1, $2, $3, $4)"
        return await self.execute(sql, telegram_id, scale_type, question_number, no_, fetchrow=True)

    async def select_sum_ayztemptemp(self, telegram_id, scale_type, column):
        sql = f"SELECT SUM({column}) FROM ayztemptemp WHERE telegram_id=$1 AND scale_type=$2"
        return await self.execute(sql, telegram_id, scale_type, fetchrow=True)

    async def select_check_ayztemptemp(self, telegram_id, question_number):
        sql = f"SELECT * FROM ayztemptemp WHERE telegram_id=$1 AND question_number=$2"
        return await self.execute(sql, telegram_id, question_number, fetchrow=True)

    async def back_user_ayztemptemp(self, telegram_id, question_number):
        await self.execute(f"DELETE FROM ayztemptemp WHERE telegram_id='{telegram_id}' "
                           f"AND question_number='{question_number}'", execute=True)

    async def delete_ayztemptemp(self, telegram_id):
        await self.execute(f"DELETE FROM ayztemptemp WHERE telegram_id='{telegram_id}'", execute=True)

    # ======================= TABLE | LEONGARD_QUESTIONS =======================
    async def add_leoquestions(self, question_number, question):
        sql = "INSERT INTO leoquestions (question_number, question) VALUES ($1, $2)"
        return await self.execute(sql, question_number, question, fetchrow=True)

    async def select_questions_leo(self):
        sql = "SELECT * FROM leoquestions ORDER BY question_number"
        return await self.execute(sql, fetch=True)

    # ======================= TABLE | LEONGARD_SCALES =======================
    async def add_leoscales(self, scale_type, yes, no_):
        sql = "INSERT INTO leoscales (scale_type, yes, no_) VALUES ($1, $2, $3)"
        return await self.execute(sql, scale_type, yes, no_, fetchrow=True)

    async def get_yes_leoscales(self, yes):
        sql = f"SELECT scale_type FROM leoscales WHERE yes={yes}"
        return await self.execute(sql, fetchrow=True)

    async def get_no_leoscales(self, no_):
        sql = f"SELECT scale_type FROM leoscales WHERE no_='{no_}'"
        return await self.execute(sql, fetchrow=True)

    # ======================= TABLE | LEONGARD_TEMPORARY =======================
    async def add_leotemp(self, telegram_id, scale_type, question_number, yes=0, no_=0):
        sql = "INSERT INTO leotemp (telegram_id, scale_type, question_number, yes, no_) VALUES ($1, $2, $3, $4, $5)"
        return await self.execute(sql, telegram_id, scale_type, question_number, yes, no_, fetchrow=True)

    async def select_check_leotemp(self, telegram_id, question_number):
        sql = f"SELECT * FROM leotemp WHERE telegram_id=$1 AND question_number=$2"
        return await self.execute(sql, telegram_id, question_number, fetchrow=True)

    async def get_sums_leotemp(self, telegram_id, scale_type):
        sql = """
        SELECT scale_type, SUM(yes) AS total_yes, SUM(no_) AS total_no 
        FROM leotemp 
        WHERE telegram_id=$1 AND scale_type=$2 
        GROUP BY scale_type
        """
        return await self.execute(sql, telegram_id, scale_type, fetchrow=True)

    async def delete_leotemp(self, telegram_id):
        await self.execute(f"DELETE FROM leotemp WHERE telegram_id='{telegram_id}'", execute=True)

    async def back_leotemp(self, telegram_id, question_number):
        await self.execute(f"DELETE FROM leotemp WHERE telegram_id='{telegram_id}' "
                           f"AND question_number='{question_number}'", execute=True)
