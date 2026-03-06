import psycopg2

def get_connection():
    return psycopg2.connect(
        host="ep-quiet-paper-ah5rgjf0-pooler.c-3.us-east-1.aws.neon.tech",
        database="prueba",
        user="neondb_owner",
        password="npg_wv2aTECu8emJ",
        port="5432",
        sslmode="require"
    )