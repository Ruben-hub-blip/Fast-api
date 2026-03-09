from fastapi import APIRouter
from app.services.ubicacion_service import obtener_localidades, obtener_barrios

router = APIRouter(prefix="/ubicaciones", tags=["Ubicaciones"])

@router.get("/localidades")
async def localidades():
    return await obtener_localidades()


@router.get("/barrios/{id_localidad}")
async def barrios(id_localidad: int):
    return await obtener_barrios(id_localidad)