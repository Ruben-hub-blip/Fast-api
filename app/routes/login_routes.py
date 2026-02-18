# app/routes/login_routes.py
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
        print(f"Intento de login para email: {user.usuario}")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar primero si el usuario existe
        cursor.execute(
            "SELECT id, email, contrasena FROM usuarios WHERE email = %s",
            (user.usuario,)
        )
        usuario_existe = cursor.fetchone()
        
        if not usuario_existe:
            print(f"Usuario no encontrado: {user.usuario}")
            raise HTTPException(
                status_code=401,
                detail="Credenciales incorrectas"
            )
        
        # Verificar contraseña
        cursor.execute(
            """
            SELECT id, email
            FROM usuarios
            WHERE email = %s AND contrasena = %s
            """,
            (user.usuario, user.contrasena)
        )
        
        result = cursor.fetchone()
        
        if not result:
            print(f"Contraseña incorrecta para: {user.usuario}")
            raise HTTPException(
                status_code=401,
                detail="Credenciales incorrectas"
            )
        
        print(f"Login exitoso para: {user.usuario}")
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

# Endpoint de prueba para verificar conexión a DB
@router.get("/test-db")
async def test_db():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        count = cursor.fetchone()[0]
        return {
            "status": "ok",
            "message": f"Conexión exitosa. {count} usuarios en la BD"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
