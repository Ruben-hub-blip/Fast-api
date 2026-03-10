from fastapi import APIRouter
from app.services.ubicacion_service import obtener_barrios

router = APIRouter()

@router.get("/barrios")
async def barrios():

    data = await obtener_barrios()

    return data