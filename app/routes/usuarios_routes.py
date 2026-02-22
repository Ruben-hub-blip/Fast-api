from fastapi import APIRouter, HTTPException
from app.config.db import get_connection

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/")
def obtener_usuarios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios")
    data = cur.fetchall()
    conn.close()
    return data


@router.get("/{id}")
def obtener_usuario(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE id=%s", (id,))
    data = cur.fetchone()
    conn.close()

    if not data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return data


@router.post("/")
def crear_usuario(usuario: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO usuarios 
        (nombre, apellido, cedula, email, contrasena, id_rol)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING *
    """, (
        usuario["nombre"],
        usuario["apellido"],
        usuario["cedula"],
        usuario["email"],
        usuario["contrasena"],
        usuario["id_rol"]
    ))

    nuevo = cur.fetchone()
    conn.commit()
    conn.close()
    return nuevo


@router.put("/{id}")
def actualizar_usuario(id: int, usuario: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE usuarios
        SET nombre=%s, apellido=%s, edad=%s
        WHERE id=%s
        RETURNING *
    """, (
        usuario["nombre"],
        usuario["apellido"],
        usuario["edad"],
        id
    ))

    actualizado = cur.fetchone()
    conn.commit()
    conn.close()

    if not actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return actualizado


@router.delete("/{id}")
def eliminar_usuario(id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM usuarios WHERE id=%s RETURNING *", (id,))
    eliminado = cur.fetchone()
    conn.commit()
    conn.close()

    if not eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"mensaje": "Usuario eliminado"}
