from fastapi import APIRouter, HTTPException
from jose import jwt
from datetime import datetime, timedelta
from app.models.user_model import UserLogin
from app.config.db_config import get_db_connection

router = APIRouter()

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login")
def login(user: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id, usuario FROM usuarios WHERE usuario = %s AND contrasena = %s",
            (user.usuario, user.contrasena)
        )

        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")

        token = create_access_token({"sub": result[1]})

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    finally:
        cursor.close()
        conn.close()



