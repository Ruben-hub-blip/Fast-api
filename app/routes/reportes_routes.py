from fastapi import APIRouter, HTTPException, Depends
from app.config.db_config import get_connection
from datetime import datetime
import httpx
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.models.user_model import ReporteCreate
from app.config.security import SECRET_KEY, ALGORITHM
from fastapi import Form, File, UploadFile
import shutil
import os

router = APIRouter(prefix="/reportes", tags=["Reportes"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Función para decodificar token y obtener datos
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

# Obtener reportes con ubicación
@router.get("/con-ubicacion")
async def obtener_reportes_con_ubicacion():
    conn = get_connection()
    cur = conn.cursor()

    # 🔥 AHORA TRAE FOTO INCLUIDA
    cur.execute("""
        SELECT 
            r.*,
            f.url AS foto
        FROM reportes r
        LEFT JOIN fotos_reporte f 
            ON r.id = f.id_reporte
    """)

    columnas = [desc[0] for desc in cur.description]
    filas = cur.fetchall()
    reportes = [dict(zip(columnas, fila)) for fila in filas]

    # 🔹 traer barrio
    async with httpx.AsyncClient() as client:
        for reporte in reportes:
            try:
                response = await client.get(
                    f"https://super-spork-x5vxjr65w4vj3pv4w-3000.app.github.dev/barrios/detalle/{reporte['id_barrio']}"
                )
                if response.status_code == 200:
                    reporte["barrio"] = response.json()
                else:
                    reporte["barrio"] = None
            except Exception as e:
                reporte["barrio"] = {"error": str(e)}

    conn.close()

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
async def crear_reporte(
    id_barrio: int = Form(...),
    descripcion: str = Form(...),
    direccion: str = Form(...),
    latitud: float = Form(...),
    longitud: float = Form(...),
    foto: UploadFile = File(None),
    current_user: dict = Depends(get_current_user)
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reportes
        (id_usuario, id_barrio, descripcion, direccion, latitud, longitud, estado, created_at)
        VALUES (%s,%s,%s,%s,%s,%s,'pendiente',%s)
        RETURNING id
    """, (
        current_user["user_id"],
        id_barrio,
        descripcion,
        direccion,
        latitud,
        longitud,
        datetime.now()
    ))

    reporte_id = cur.fetchone()[0]

    url_imagen = None

    if foto:

        filename = f"{reporte_id}_{foto.filename}"
        filepath = f"uploads/{filename}"

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(foto.file, buffer)

        url_imagen = f"/uploads/{filename}"

        cur.execute("""
            INSERT INTO fotos_reporte (id_reporte, url)
            VALUES (%s,%s)
        """,(reporte_id,url_imagen))

    conn.commit()
    conn.close()

    return {
        "mensaje":"Reporte creado",
        "id":reporte_id,
        "foto":url_imagen
    }


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


