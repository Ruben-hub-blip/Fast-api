from fastapi import APIRouter, HTTPException
from app.config.db_config import get_connection
from datetime import datetime

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# ✅ Obtener todos
@router.get("/")
def obtener_usuarios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios")
    data = cur.fetchall()
    conn.close()
    return data


# ✅ Obtener por ID
@router.get("/{id}")
def obtener_usuario(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cur.fetchone()
    conn.close()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario


# ✅ Crear usuario
@router.post("/")
def crear_usuario(
    nombre: str,
    apellido: str,
    cedula: str,
    edad: int,
    email: str,
    contrasena: str,
    id_rol: int,
    id_barrio: int
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO usuarios 
        (nombre, apellido, cedula, edad, email, contrasena, id_rol, id_barrio)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (nombre, apellido, cedula, edad, email, contrasena, id_rol, id_barrio))

    nuevo_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    return {"mensaje": "Usuario creado", "id": nuevo_id}


# ✅ Actualizar usuario
@router.put("/{id}")
def actualizar_usuario(
    id: int,
    nombre: str,
    apellido: str,
    edad: int,
    email: str,
    id_rol: int,
    id_barrio: int,
    estado: str
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE usuarios
        SET nombre=%s,
            apellido=%s,
            edad=%s,
            email=%s,
            id_rol=%s,
            id_barrio=%s,
            estado=%s,
            updated_at=%s
        WHERE id=%s
    """, (
        nombre,
        apellido,
        edad,
        email,
        id_rol,
        id_barrio,
        estado,
        datetime.now(),
        id
    ))

    conn.commit()
    conn.close()

    return {"mensaje": "Usuario actualizado"}


# ✅ Eliminar usuario
@router.delete("/{id}")
def eliminar_usuario(id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM usuarios WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    return {"mensaje": "Usuario eliminado"}