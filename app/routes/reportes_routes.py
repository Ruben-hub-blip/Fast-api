from fastapi import APIRouter
from app.config.db import get_connection

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("/")
def obtener_reportes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM reportes")
    data = cur.fetchall()
    conn.close()
    return data
