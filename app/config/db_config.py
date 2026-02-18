# db_config.py
import psycopg2
import os
from urllib.parse import urlparse, parse_qs

def get_db_connection():
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL no está configurada en las variables de entorno")

    url = urlparse(dsn)
    query_params = parse_qs(url.query)

    return psycopg2.connect(
        dbname=url.path[1:],          # quita el "/" inicial
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port,
        sslmode=query_params.get("sslmode", ["require"])[0]  # usa sslmode=require por defecto
    )



