# app/routes/login_routes.py
from fastapi import APIRouter, HTTPException
from jose import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr, Field
from app.config.db_config import get_db_connection
import traceback

router = APIRouter()

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Crear un modelo que acepte ambos formatos
class UserLoginFlexible(BaseModel):
    usuario: EmailStr = Field(None, alias="username")  # Acepta 'username' como alias
    contrasena: str = Field(None, alias="contraseña")  # Acepta 'contraseña' como alias
    username: EmailStr = None  # Campo opcional
    contraseña: str = None     # Campo opcional
    
    class Config:
        populate_by_name = True  # Permite usar los nombres originales o los alias

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login")
async def login(user_data: UserLoginFlexible):
    conn = None
    cursor = None
    
    try:
        # Determinar qué campo de usuario usar
        email = user_data.usuario or user_data.username
        password = user_data.contrasena or user_data.contraseña
        
        if not email or not password:
            raise HTTPException(
                status_code=400,
                detail="Debe proporcionar email y contraseña"
            )
        
        print(f"Intento de login para email: {email}")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar credenciales
        cursor.execute(
            """
            SELECT id, email
            FROM usuarios
            WHERE email = %s AND contrasena = %s
            """,
            (email, password)
        )
        
        result = cursor.fetchone()
        
        if not result:
            print(f"Credenciales incorrectas para: {email}")
            raise HTTPException(
                status_code=401,
                detail="Credenciales incorrectas"
            )
        
        print(f"Login exitoso para: {email}")
        token = create_access_token({"sub": result[1]})
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": result[0]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en login: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
