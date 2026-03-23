from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.config.db_config import get_connection
from app.config.security import create_access_token
import httpx

router = APIRouter()

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    password = form_data.password

    conn = get_connection()
    cur = conn.cursor()

    # 🔥 AHORA TRAEMOS EL NOMBRE
    cur.execute("""
        SELECT id, nombre, email, contrasena, id_rol, id_barrio
        FROM usuarios
        WHERE email=%s
    """, (email,))

    user = cur.fetchone()

    if not user:
        cur.close()
        conn.close()
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    # 🔥 IMPORTANTE: ahora incluye nombre
    user_id, nombre, email_db, password_db, rol_id, id_barrio = user

    if password != password_db:
        cur.close()
        conn.close()
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # 🔹 Obtener nombre del barrio desde Express
    nombre_barrio = "Sin barrio"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://super-spork-x5vxjr65w4vj3pv4w-3000.app.github.dev/barrios/detalle/{id_barrio}"
            )

            if response.status_code == 200:
                data = response.json()
                nombre_barrio = data.get("nombre", "Sin barrio")

    except Exception as e:
        print("Error obteniendo barrio:", e)

    # 🔹 Obtener módulos
    cur.execute("""
        SELECT m.nombre
        FROM rol_modulo rm
        JOIN modulos m ON rm.id_modulo = m.id
        WHERE rm.id_rol=%s AND rm.estado='activo'
    """, (rol_id,))

    modulos = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()

    # 🔥 TOKEN COMPLETO (YA CON NOMBRE)
    access_token = create_access_token(
        data={
            "sub": email_db,
            "user_id": user_id,
            "nombre": nombre,        # 👈 CLAVE
            "rol_id": rol_id,
            "id_barrio": id_barrio,
            "barrio": nombre_barrio,
            "modulos": modulos
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }