from fastapi import APIRouter
from app.config.db import get_connection

router = APIRouter(prefix="/comentarios", tags=["Comentarios"])

@router.get("/")
def obtener_comentarios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM comentarios_reportes")
    data = cur.fetchall()
    conn.close()
    return data
