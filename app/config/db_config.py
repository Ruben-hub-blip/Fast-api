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
        dbname=url.path[1:],          # "prueba"
        user=url.username,            # "neondb_owner"
        password=url.password,        # tu contraseña
        host=url.hostname,            # ep-quiet-paper-ah5rgjf0-pooler.c-3.us-east-1.aws.neon.tech
        port=url.port or 5432,
        sslmode=query_params.get("sslmode", ["require"])[0]
    )



