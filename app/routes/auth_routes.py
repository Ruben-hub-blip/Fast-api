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
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, email, contrasena, id_rol FROM usuarios WHERE email = %s",
        (email,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    if user[2] != password:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    access_token = create_access_token(
        data={
            "sub": user[1],
            "user_id": user[0],
            "rol_id": user[3]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }