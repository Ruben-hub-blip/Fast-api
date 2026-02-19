from fastapi import APIRouter, HTTPException
from jose import jwt
from datetime import datetime, timedelta
from app.models.user_model import UserLogin
from app.config.db_config import get_db_connection
import traceback

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
async def login(user: UserLogin):
    conn = None
    cursor = None
    
    try:
        print(f" Login intent - Email: {user.usuario}")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si el usuario existe
        cursor.execute(
            "SELECT id, email, contrasena FROM usuarios WHERE email = %s",
            (user.usuario,)
        )
        db_user = cursor.fetchone()
        
        if not db_user:
            print(f" Usuario no encontrado: {user.usuario}")
            raise HTTPException(
                status_code=401,
                detail="Credenciales incorrectas"
            )
        
        print(f" Usuario encontrado: {db_user[1]}")
        print(f" Contraseña DB: {db_user[2]}, Recibida: {user.contrasena}")
        
        # Verificar contraseña
        if db_user[2] != user.contrasena:
            print(" Contraseña incorrecta")
            raise HTTPException(
                status_code=401,
                detail="Credenciales incorrectas"
            )
        
        # Todo bien, crear token
        token = create_access_token({"sub": db_user[1]})
        print(f" Login exitoso para: {user.usuario}")
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": db_user[0]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}"
        )
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Endpoint de prueba
@router.get("/login-test")
async def login_test():
    return {"mensaje": "Endpoint de login funcionando"}
