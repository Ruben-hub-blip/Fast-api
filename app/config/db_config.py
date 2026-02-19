import psycopg2
import os
from psycopg2.extras import RealDictCursor

def get_db_connection():
   
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL no esta configurada")
    
    try:
        conn = psycopg2.connect(dsn)
        return conn
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        raise e

def get_db_connection_dict():
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL no está configurada")
    
    try:
        conn = psycopg2.connect(dsn, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        raise e



