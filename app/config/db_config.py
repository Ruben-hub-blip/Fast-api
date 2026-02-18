# app/config/db_config.py
import psycopg2
import os
from urllib.parse import urlparse, parse_qs

def get_db_connection():
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL no está configurada en las variables de entorno")

    print("DATABASE_URL:", dsn)  # Log temporal para verificar

    url = urlparse(dsn)
    query_params = parse_qs(url.query)

    # Construimos manualmente la cadena de conexión para evitar que psycopg2
    # intente usar el socket local
    conn_str = (
        f"dbname={url.path[1:]} "
        f"user={url.username} "
        f"password={url.password} "
        f"host={url.hostname} "
        f"port={url.port or 5432} "
        f"sslmode={query_params.get('sslmode', ['require'])[0]}"
    )

    print("Connection string:", conn_str)  # Verifica que host y puerto estén correctos

    return psycopg2.connect(conn_str)


