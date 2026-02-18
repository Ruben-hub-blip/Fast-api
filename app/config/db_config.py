import psycopg2
import os

def get_db_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise Exception("DATABASE_URL no configurada")

    return psycopg.connect(database_url)



