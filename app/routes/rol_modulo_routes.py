from fastapi import APIRouter, HTTPException
from app.config.db_config import get_connection
from datetime import datetime

router = APIRouter(prefix="/rol_modulo", tags=["Rol_Modulo"])

# ✅ Obtener todos
@router.get("/")
def obtener_rol_modulo():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rol_modulo")
    data = cur.fetchall()
    conn.close()
    return data


# ✅ Crear relación
@router.post("/")
def crear_rol_modulo(id_rol: int, id_modulo: int, estado: str = "activo"):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO rol_modulo 
            (id_rol, id_modulo, estado, created_at)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (id_rol, id_modulo, estado, datetime.now()))

        nuevo_id = cur.fetchone()[0]
        conn.commit()
        return {"mensaje": "Relación creada", "id": nuevo_id}

    except Exception:
        conn.rollback()
        raise HTTPException(status_code=400, detail="La relación ya existe")

    finally:
        conn.close()


# ✅ Eliminar relación
@router.delete("/{id}")
def eliminar_rol_modulo(id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM rol_modulo WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    return {"mensaje": "Relación eliminada"}