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

    # Extraer valores correctamente
    dbname = url.path.lstrip("/")   # "prueba"
    user = url.username             # "neondb_owner"
    password = url.password         # tu contraseña
    host = url.hostname             # host de NeonDB
    port = url.port or 5432
    sslmode = query_params.get("sslmode", ["require"])[0]

    conn_str = (
        f"dbname={dbname} "
        f"user={user} "
        f"password={password} "
        f"host={host} "
        f"port={port} "
        f"sslmode={sslmode}"
    )

    print("Connection string:", conn_str)

    return psycopg2.connect(conn_str)

