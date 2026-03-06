from fastapi import APIRouter, HTTPException
from app.config.db_config import get_connection
from datetime import datetime

router = APIRouter(prefix="/reportes", tags=["Reportes"])

# ✅ Obtener todos
@router.get("/")
def obtener_reportes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM reportes")
    data = cur.fetchall()
    conn.close()
    return data


# ✅ Obtener por ID
@router.get("/{id}")
def obtener_reporte(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM reportes WHERE id=%s", (id,))
    reporte = cur.fetchone()
    conn.close()

    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    return reporte


# ✅ Crear
@router.post("/")
def crear_reporte(
    id_usuario: int,
    id_barrio: int,
    descripcion: str,
    direccion: str
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reportes
        (id_usuario, id_barrio, descripcion, direccion, estado, created_at)
        VALUES (%s, %s, %s, %s, 'pendiente', %s)
        RETURNING id
    """, (id_usuario, id_barrio, descripcion, direccion, datetime.now()))

    nuevo_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    return {"mensaje": "Reporte creado", "id": nuevo_id}


# ✅ Actualizar
@router.put("/{id}")
def actualizar_reporte(
    id: int,
    descripcion: str,
    direccion: str,
    estado: str
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE reportes
        SET descripcion=%s,
            direccion=%s,
            estado=%s,
            updated_at=%s
        WHERE id=%s
    """, (descripcion, direccion, estado, datetime.now(), id))

    conn.commit()
    conn.close()

    return {"mensaje": "Reporte actualizado"}


# ✅ Eliminar
@router.delete("/{id}")
def eliminar_reporte(id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM reportes WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    return {"mensaje": "Reporte eliminado"}