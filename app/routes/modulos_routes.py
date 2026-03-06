from fastapi import APIRouter, HTTPException
from app.config.db_config import get_connection
from datetime import datetime

router = APIRouter(prefix="/modulos", tags=["Modulos"])

# ✅ Obtener todos
@router.get("/")
def obtener_modulos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM modulos")
    data = cur.fetchall()
    conn.close()
    return data


# ✅ Obtener por ID
@router.get("/{id}")
def obtener_modulo(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM modulos WHERE id=%s", (id,))
    modulo = cur.fetchone()
    conn.close()

    if not modulo:
        raise HTTPException(status_code=404, detail="Modulo no encontrado")

    return modulo


# ✅ Crear
@router.post("/")
def crear_modulo(nombre: str, estado: str = "activo"):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO modulos (nombre, estado, created_at)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (nombre, estado, datetime.now()))

    nuevo_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    return {"mensaje": "Modulo creado", "id": nuevo_id}


# ✅ Actualizar
@router.put("/{id}")
def actualizar_modulo(id: int, nombre: str, estado: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE modulos
        SET nombre=%s,
            estado=%s,
            updated_at=%s
        WHERE id=%s
    """, (nombre, estado, datetime.now(), id))

    conn.commit()
    conn.close()

    return {"mensaje": "Modulo actualizado"}


# ✅ Eliminar
@router.delete("/{id}")
def eliminar_modulo(id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM modulos WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    return {"mensaje": "Modulo eliminado"}
