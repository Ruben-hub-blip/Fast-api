from fastapi import APIRouter
from app.config.db import get_connection

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/")
def obtener_roles():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM roles")
    data = cur.fetchall()
    conn.close()
    return data
