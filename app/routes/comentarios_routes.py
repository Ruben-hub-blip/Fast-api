from fastapi import APIRouter, HTTPException, Depends
from app.config.db_config import get_connection
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

router = APIRouter(prefix="/comentarios", tags=["Comentarios"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "YOUR_SECRET_KEY"  # Debe coincidir con security.py

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
    rol_id = current_user["rol_id"]
    id_barrio = current_user["id_barrio"]

    if rol_id == 1:  # Ciudadano
        cur.execute("""
            SELECT c.* 
            FROM comentarios_reportes c
            JOIN reportes r ON c.id_reporte = r.id
            WHERE r.id_barrio = %s
        """, (id_barrio,))
    elif rol_id == 2:  # Líder
        cur.execute("""
            SELECT c.* 
            FROM comentarios_reportes c
            JOIN reportes r ON c.id_reporte = r.id
            WHERE r.id_barrio = %s
        """, (id_barrio,))
    else:  # Admin
        cur.execute("SELECT * FROM comentarios_reportes")

    columnas = [desc[0] for desc in cur.description]
    filas = cur.fetchall()
    comentarios = [dict(zip(columnas, f)) for f in filas]
    conn.close()
    return comentarios

# ✅ Crear
@router.post("/")
def crear_comentario(
    id_reporte: int,
    comentario: str,
    current_user: dict = Depends(get_current_user)
):
    conn = get_connection()
    cur = conn.cursor()

    # Validar barrio del reporte
    cur.execute("SELECT id_barrio FROM reportes WHERE id=%s", (id_reporte,))
    res = cur.fetchone()
    if not res:
        conn.close()
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    id_barrio_reporte = res[0]

    if current_user["rol_id"] in [1,2] and current_user["id_barrio"] != id_barrio_reporte:
        conn.close()
        raise HTTPException(status_code=403, detail="No puede comentar en este reporte")

    cur.execute("""
        INSERT INTO comentarios_reportes (id_reporte, id_usuario, comentario)
        VALUES (%s, %s, %s) RETURNING id
    """, (id_reporte, current_user["user_id"], comentario))

    nuevo_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    return {"mensaje": "Comentario creado", "id": nuevo_id}

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