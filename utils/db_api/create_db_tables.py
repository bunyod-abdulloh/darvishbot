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
                return None
            return None
        return None

    async def create_tables(self):
        """Create the required tables in the database."""
        queries = [
            """
            CREATE TABLE IF NOT EXISTS bot_users (
                id SERIAL PRIMARY KEY,                
                telegram_id VARCHAR(50) NOT NULL UNIQUE,
                gender VARCHAR(5) NULL,
                age VARCHAR(5) NULL                                
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS bot_send_status (
                id SERIAL PRIMARY KEY,
                send_post BOOLEAN DEFAULT FALSE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS bot_articles (
                id SERIAL PRIMARY KEY NOT NULL,
                file_name VARCHAR(150) NULL,
                link VARCHAR(150) NULL        
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS bot_medias (
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
            CREATE TABLE IF NOT EXISTS bot_tt_yaxin(
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
            CREATE TABLE IF NOT EXISTS bot_yaxinscales (
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
            CREATE TABLE IF NOT EXISTS bot_tempyaxin (
                id SERIAL PRIMARY KEY,                     
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
            CREATE TABLE IF NOT EXISTS bot_yaxinanswers (
                id SERIAL PRIMARY KEY,                
                full_name VARCHAR(255) NOT NULL,
                telegram_id BIGINT NOT NULL,
                test_type VARCHAR(50) NOT NULL,
                scale_type VARCHAR(50) NULL,
                all_points NUMERIC NULL                        
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS bot_ayztempquestions (
                id SERIAL PRIMARY KEY,                  
                question_number INTEGER NOT NULL,           
                question TEXT NOT NULL                                    
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS bot_ayztempscales (  
                id SERIAL PRIMARY KEY,              
                scale_type VARCHAR(50) NOT NULL,       
                yes INTEGER NOT NULL,           
                no_ INTEGER NOT NULL                                    
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS bot_ayztemptemp (                 
                telegram_id BIGINT NOT NULL,              
                scale_type VARCHAR(50) NULL,
                question_number INTEGER NULL,       
                yes INTEGER NULL,           
                no_ INTEGER NULL                                    
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS bot_leoquestions (                          
                question_number INTEGER NOT NULL,                   
                question TEXT NOT NULL                                            
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS bot_leoscales (                          
                id SERIAL PRIMARY KEY,
                scale_type VARCHAR(15) NOT NULL,        
                yes INTEGER NULL,
                no_ INTEGER NULL                                    
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS bot_leotemp (                
                telegram_id BIGINT NOT NULL,              
                scale_type VARCHAR(50) NULL,
                question_number INTEGER NULL,       
                yes INTEGER DEFAULT 0,            
                no_ INTEGER DEFAULT 0                                                    
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS bot_statistics (
                id SERIAL PRIMARY KEY,
                created_at DATE DEFAULT CURRENT_DATE,
                user_id BIGINT NOT NULL REFERENCES bot_users(id),
                test_type VARCHAR(255) NOT NULL,
                result VARCHAR(500),
                UNIQUE (user_id, test_type)
            );
            """
        ]
        # Execute each table creation query
        for query in queries:
            await self.execute(query, execute=True)
