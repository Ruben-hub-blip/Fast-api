from fastapi import APIRouter, HTTPException, Depends
from app.config.db_config import get_connection
from datetime import datetime
import httpx
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

router = APIRouter(prefix="/reportes", tags=["Reportes"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "YOUR_SECRET_KEY"  # Debe coincidir con tu security.py

# Función para decodificar token y obtener datos
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

# Obtener reportes con ubicación
@router.get("/con-ubicacion")
async def obtener_reportes_con_ubicacion(current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cur = conn.cursor()

    rol_id = current_user["rol_id"]
    id_barrio = current_user["id_barrio"]

    # Ciudadano: solo reportes de su barrio
    if rol_id == 1:
        cur.execute("SELECT * FROM reportes WHERE id_barrio=%s", (id_barrio,))
    # Líder: reportes de su barrio
    elif rol_id == 2:
        cur.execute("SELECT * FROM reportes WHERE id_barrio=%s", (id_barrio,))
    # Admin: todos los reportes
    else:
        cur.execute("SELECT * FROM reportes")

    columnas = [desc[0] for desc in cur.description]
    filas = cur.fetchall()
    reportes = [dict(zip(columnas, fila)) for fila in filas]

    conn.close()

    # Obtener info de barrio y localidad
    async with httpx.AsyncClient() as client:
        for reporte in reportes:
            try:
                response = await client.get(
                    f"https://super-spork-x5vxjr65w4vj3pv4w-3000.app.github.dev/barrios/{reporte['id_barrio']}"
                )
                if response.status_code == 200:
                    reporte["barrio"] = response.json()
                else:
                    reporte["barrio"] = None
            except Exception as e:
                reporte["barrio"] = {"error": str(e)}

    return reportes

# CRUD normal
@router.get("/")
def obtener_reportes(current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM reportes")
    columnas = [desc[0] for desc in cur.description]
    filas = cur.fetchall()
    reportes = [dict(zip(columnas, fila)) for fila in filas]
    conn.close()
    return reportes

@router.get("/{id}")
def obtener_reporte(id: int, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM reportes WHERE id=%s", (id,))
    fila = cur.fetchone()
    if not fila:
        conn.close()
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    columnas = [desc[0] for desc in cur.description]
    reporte = dict(zip(columnas, fila))
    conn.close()
    return reporte

@router.post("/")
def crear_reporte(
    id_usuario: int,
    id_barrio: int,
    descripcion: str,
    direccion: str,
    current_user: dict = Depends(get_current_user)
):
    # Validar que ciudadano solo cree reportes en su barrio
    if current_user["rol_id"] == 1 and current_user["id_barrio"] != id_barrio:
        raise HTTPException(status_code=403, detail="No puede crear reportes fuera de su barrio")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO reportes
        (id_usuario, id_barrio, descripcion, direccion, estado, created_at)
        VALUES (%s, %s, %s, %s, 'pendiente', %s)
        RETURNING id
    """, (id_usuario, id_barrio, descripcion, direccion, datetime.now()))
    nuevo_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return {"mensaje": "Reporte creado", "id": nuevo_id}

@router.put("/{id}")
def actualizar_reporte(id: int, descripcion: str, direccion: str, estado: str, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE reportes
        SET descripcion=%s,
            direccion=%s,
            estado=%s,
            updated_at=%s
        WHERE id=%s
    """, (descripcion, direccion, estado, datetime.now(), id))
    conn.commit()
    conn.close()
    return {"mensaje": "Reporte actualizado"}

@router.delete("/{id}")
def eliminar_reporte(id: int, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM reportes WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return {"mensaje": "Reporte eliminado"}


