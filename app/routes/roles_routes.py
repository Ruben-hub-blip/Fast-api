from fastapi import APIRouter, HTTPException
from app.config.db_config import get_connection
from datetime import datetime

router = APIRouter(prefix="/roles", tags=["Roles"])

# ✅ Obtener todos
@router.get("/")
def obtener_roles():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM roles")

    columnas = [desc[0] for desc in cur.description]
    filas = cur.fetchall()

    roles = [dict(zip(columnas, fila)) for fila in filas]

    conn.close()

    return roles


# ✅ Obtener por ID
@router.get("/{id}")
def obtener_role(id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM roles WHERE id=%s", (id,))
    fila = cur.fetchone()

    if not fila:
        conn.close()
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    columnas = [desc[0] for desc in cur.description]
    role = dict(zip(columnas, fila))

    conn.close()

    return role

# ✅ Crear
@router.post("/")
def crear_role(nombre: str, estado: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO roles (nombre, estado, created_at)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (nombre, estado, datetime.now()))

    nuevo_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    return {"mensaje": "Role creado", "id": nuevo_id}


# ✅ Actualizar
@router.put("/{id}")
def actualizar_role(id: int, nombre: str, estado: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE roles
        SET nombre=%s,
            estado=%s,
            updated_at=%s
        WHERE id=%s
    """, (nombre, estado, datetime.now(), id))

    conn.commit()
    conn.close()

    return {"mensaje": "Role actualizado"}


# ✅ Eliminar
@router.delete("/{id}")
def eliminar_role(id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM roles WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    return {"mensaje": "Role eliminado"}
