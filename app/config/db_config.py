# app/config/db_config.py
import psycopg2
import os

def get_db_connection():
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL no está configurada en las variables de entorno")
    
    print("DATABASE_URL:", dsn)  # Log temporal
    
    # ¡Directamente! psycopg2 entiende el formato postgresql://
    return psycopg2.connect(dsn)

