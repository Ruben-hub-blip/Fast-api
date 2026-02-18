# app/config/db_config.py
import psycopg2
import os
from urllib.parse import urlparse, parse_qs

def get_db_connection():
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL no está configurada en las variables de entorno")

    print("DATABASE_URL:", dsn)  # Log temporal

    url = urlparse(dsn)
    query_params = parse_qs(url.query)

    dbname = url.path.lstrip("/")  # quitar la barra inicial

    conn_str = (
        f"dbname={dbname} "
        f"user={url.username} "
        f"password={url.password} "
        f"host={url.hostname} "
        f"port={url.port or 5432} "
        f"sslmode={query_params.get('sslmode', ['require'])[0]}"
    )

    print("Connection string:", conn_str)

    return psycopg2.connect(conn_str)

