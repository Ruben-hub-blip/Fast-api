from fastapi import APIRouter
from app.config.db import get_connection

router = APIRouter(prefix="/modulos", tags=["Modulos"])

@router.get("/")
def obtener_modulos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM modulos")
    data = cur.fetchall()
    conn.close()
    return data
