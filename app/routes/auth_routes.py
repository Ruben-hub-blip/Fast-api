from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.config.db_config import get_connection
from app.config.security import create_access_token

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    password = form_data.password

    conn = get_connection()
    cur = conn.cursor()

    # Obtener usuario
    cur.execute(
        "SELECT id, email, contrasena, id_rol, id_barrio FROM usuarios WHERE email=%s",
        (email,)
    )
    user = cur.fetchone()

    if not user:
        cur.close()
        conn.close()
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    user_id, email_db, password_db, rol_id, id_barrio = user

    if password != password_db:
        cur.close()
        conn.close()
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # Obtener módulos del rol
    cur.execute("""
        SELECT m.nombre
        FROM rol_modulo rm
        JOIN modulos m ON rm.id_modulo = m.id
        WHERE rm.id_rol=%s AND rm.estado='activo'
    """, (rol_id,))
    modulos = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()

    access_token = create_access_token(
        data={
            "sub": email_db,
            "user_id": user_id,
            "rol_id": rol_id,
            "id_barrio": id_barrio,
            "modulos": modulos
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }