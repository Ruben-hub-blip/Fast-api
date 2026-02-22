from fastapi import APIRouter
from app.config.db import get_connection

router = APIRouter(prefix="/historial", tags=["Historial"])

@router.get("/")
def obtener_historial():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM historial_reportes")
    data = cur.fetchall()
    conn.close()
    return data
