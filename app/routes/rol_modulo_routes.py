from fastapi import APIRouter
from app.config.db import get_connection

router = APIRouter(prefix="/rol-modulo", tags=["Rol_Modulo"])

@router.get("/")
def obtener_relaciones():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rol_modulo")
    data = cur.fetchall()
    conn.close()
    return data
