import psycopg
import os

def get_db_connection():
    return psycopg.connect(
        os.getenv("DATABASE_URL")
    )
