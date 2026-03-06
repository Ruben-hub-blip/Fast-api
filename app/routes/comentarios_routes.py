from fastapi import APIRouter, HTTPException
from app.config.db_config import get_connection

router = APIRouter(prefix="/comentarios", tags=["Comentarios"])

# ✅ Obtener todos
@router.get("/")
def obtener_comentarios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM comentarios_reportes")
    data = cur.fetchall()
    conn.close()
    return data


# ✅ Crear
@router.post("/")
def crear_comentario(
    id_reporte: int,
    id_foto: int,
    id_usuario: int,
    comentario: str
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO comentarios_reportes
        (id_reporte, id_foto, id_usuario, comentario)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (id_reporte, id_foto, id_usuario, comentario))

    nuevo_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    return {"mensaje": "Comentario creado", "id": nuevo_id}


# ✅ Eliminar
@router.delete("/{id}")
def eliminar_comentario(id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM comentarios_reportes WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    return {"mensaje": "Comentario eliminado"}