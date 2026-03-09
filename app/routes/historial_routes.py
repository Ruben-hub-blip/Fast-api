from fastapi import APIRouter, HTTPException, Depends
from app.config.db_config import get_connection
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

router = APIRouter(prefix="/historial", tags=["Historial_Reportes"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "YOUR_SECRET_KEY"

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

# ✅ Obtener historial
@router.get("/")
def obtener_historial(current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cur = conn.cursor()
    rol_id = current_user["rol_id"]
    id_barrio = current_user["id_barrio"]

    if rol_id == 1:  # Ciudadano: solo sus reportes
        cur.execute("""
            SELECT h.*
            FROM historial_reportes h
            JOIN reportes r ON h.id_reporte = r.id
            WHERE r.id_usuario = %s
        """, (current_user["user_id"],))
    elif rol_id == 2:  # Líder: historial de su barrio
        cur.execute("""
            SELECT h.*
            FROM historial_reportes h
            JOIN reportes r ON h.id_reporte = r.id
            WHERE r.id_barrio = %s
        """, (id_barrio,))
    else:  # Admin
        cur.execute("SELECT * FROM historial_reportes")

    columnas = [desc[0] for desc in cur.description]
    filas = cur.fetchall()
    historial = [dict(zip(columnas, f)) for f in filas]
    conn.close()
    return historial

# ✅ Crear historial
@router.post("/")
def crear_historial(
    id_reporte: int,
    estado_anterior: str,
    estado_nuevo: str,
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
        raise HTTPException(status_code=403, detail="No puede registrar historial de este reporte")

    cur.execute("""
        INSERT INTO historial_reportes (id_reporte, estado_anterior, estado_nuevo, cambiado_por, fecha_cambio)
        VALUES (%s, %s, %s, %s, %s) RETURNING id
    """, (id_reporte, estado_anterior, estado_nuevo, current_user["user_id"], datetime.now()))

    nuevo_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return {"mensaje": "Historial registrado", "id": nuevo_id}
