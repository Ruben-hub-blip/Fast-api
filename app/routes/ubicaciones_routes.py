from fastapi import APIRouter
from app.services.ubicacion_service import obtener_localidades, obtener_barrios

router = APIRouter()

@router.get("/localidades")
async def localidades():
    return await obtener_localidades()


@router.get("/barrios")
async def barrios():
    return await obtener_barrios()