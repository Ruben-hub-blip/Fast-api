from fastapi import APIRouter, HTTPException, Depends
from app.config.db_config import get_connection
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

router = APIRouter(prefix="/comentarios", tags=["Comentarios"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
from app.config.security import SECRET_KEY  # Debe coincidir con security.py

# Función para decodificar token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

# ✅ Obtener todos
@router.get("/")
def obtener_comentarios(current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            c.id,
            c.id_reporte,
            c.id_usuario,
            c.comentario,
            c.created_at,
            u.nombre AS usuario_nombre
        FROM comentarios_reportes c
        JOIN usuarios u ON c.id_usuario = u.id
        ORDER BY c.created_at DESC
    """)

    columnas = [desc[0] for desc in cur.description]
    filas = cur.fetchall()
    comentarios = [dict(zip(columnas, f)) for f in filas]

    conn.close()
    return comentarios

# ✅ Crear
from pydantic import BaseModel

class ComentarioCreate(BaseModel):
    id_reporte: int
    comentario: str

@router.post("/")
def crear_comentario(
    data: ComentarioCreate,
    current_user: dict = Depends(get_current_user)
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO comentarios_reportes (id_reporte, id_usuario, comentario)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (
        data.id_reporte,
        current_user["user_id"],
        data.comentario
    ))

    conn.commit()
    conn.close()

    return {"mensaje": "Comentario creado"}

# ✅ Eliminar
@router.delete("/{id}")
def eliminar_comentario(id: int, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cur = conn.cursor()

    # Validar que exista y su barrio
    cur.execute("""
        SELECT r.id_barrio FROM comentarios_reportes c
        JOIN reportes r ON c.id_reporte = r.id
        WHERE c.id=%s
    """, (id,))
    res = cur.fetchone()
    if not res:
        conn.close()
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    id_barrio_reporte = res[0]

    if current_user["rol_id"] in [1,2] and current_user["id_barrio"] != id_barrio_reporte:
        conn.close()
        raise HTTPException(status_code=403, detail="No puede eliminar este comentario")

    cur.execute("DELETE FROM comentarios_reportes WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return {"mensaje": "Comentario eliminado"}