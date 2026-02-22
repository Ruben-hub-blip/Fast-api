from fastapi import APIRouter
from app.config.db import get_connection

router = APIRouter(prefix="/fotos", tags=["Fotos"])

@router.get("/")
def obtener_fotos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM fotos_reporte")
    data = cur.fetchall()
    conn.close()
    return data
