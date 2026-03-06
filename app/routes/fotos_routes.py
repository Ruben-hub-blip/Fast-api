from fastapi import APIRouter, HTTPException
from app.config.db_config import get_connection

router = APIRouter(prefix="/fotos", tags=["Fotos"])

# ✅ Obtener todas
@router.get("/")
def obtener_fotos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM fotos_reporte")
    data = cur.fetchall()
    conn.close()
    return data


# ✅ Crear
@router.post("/")
def crear_foto(
    id_reporte: int,
    url: str,
    estado: str = "activo"
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO fotos_reporte (id_reporte, url, estado)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (id_reporte, url, estado))

    nuevo_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    return {"mensaje": "Foto agregada", "id": nuevo_id}


# ✅ Eliminar
@router.delete("/{id}")
def eliminar_foto(id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM fotos_reporte WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    return {"mensaje": "Foto eliminada"}
