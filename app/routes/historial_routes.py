from fastapi import APIRouter
from app.config.db_config import get_connection
from datetime import datetime

router = APIRouter(prefix="/historial", tags=["Historial_Reportes"])

# ✅ Obtener todo el historial
@router.get("/")
def obtener_historial():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM historial_reportes")
    data = cur.fetchall()
    conn.close()
    return data


# ✅ Crear registro de cambio
@router.post("/")
def crear_historial(
    id_reporte: int,
    estado_anterior: str,
    estado_nuevo: str,
    cambiado_por: int
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO historial_reportes
        (id_reporte, estado_anterior, estado_nuevo, cambiado_por, fecha_cambio)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """, (
        id_reporte,
        estado_anterior,
        estado_nuevo,
        cambiado_por,
        datetime.now()
    ))

    nuevo_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    return {"mensaje": "Historial registrado", "id": nuevo_id}
