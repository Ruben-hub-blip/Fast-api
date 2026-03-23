from fastapi import APIRouter, HTTPException, Depends
from app.config.db_config import get_connection
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

router = APIRouter(prefix="/fotos", tags=["Fotos"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
from app.config.security import SECRET_KEY

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

# ✅ Obtener todas
@router.get("/")
def obtener_fotos(current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cur = conn.cursor()
    rol_id = current_user["rol_id"]
    id_barrio = current_user["id_barrio"]

    if rol_id in [1,2]:
        cur.execute("""
            SELECT f.* 
            FROM fotos_reporte f
            JOIN reportes r ON f.id_reporte = r.id
            WHERE r.id_barrio = %s
        """, (id_barrio,))
    else:
        cur.execute("SELECT * FROM fotos_reporte")

    columnas = [desc[0] for desc in cur.description]
    filas = cur.fetchall()
    fotos = [dict(zip(columnas, f)) for f in filas]
    conn.close()
    return fotos

# ✅ Crear
@router.post("/")
def crear_foto(
    id_reporte: int,
    url: str,
    estado: str = "activo",
    current_user: dict = Depends(get_current_user)
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id_barrio FROM reportes WHERE id=%s", (id_reporte,))
    res = cur.fetchone()
    if not res:
        conn.close()
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    id_barrio_reporte = res[0]

    if current_user["rol_id"] in [1,2] and current_user["id_barrio"] != id_barrio_reporte:
        conn.close()
        raise HTTPException(status_code=403, detail="No puede subir foto a este reporte")

    cur.execute("""
        INSERT INTO fotos_reporte (id_reporte, url, estado)
        VALUES (%s, %s, %s) RETURNING id
    """, (id_reporte, url, estado))
    nuevo_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return {"mensaje": "Foto agregada", "id": nuevo_id}

# ✅ Eliminar
@router.delete("/{id}")
def eliminar_foto(id: int, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT r.id_barrio FROM fotos_reporte f
        JOIN reportes r ON f.id_reporte = r.id
        WHERE f.id=%s
    """, (id,))
    res = cur.fetchone()
    if not res:
        conn.close()
        raise HTTPException(status_code=404, detail="Foto no encontrada")
    id_barrio_reporte = res[0]

    if current_user["rol_id"] in [1,2] and current_user["id_barrio"] != id_barrio_reporte:
        conn.close()
        raise HTTPException(status_code=403, detail="No puede eliminar esta foto")

    cur.execute("DELETE FROM fotos_reporte WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return {"mensaje": "Foto eliminada"}
