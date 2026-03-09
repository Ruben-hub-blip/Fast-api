import httpx

BASE_URL = "https://super-spork-x5vxjr65w4vj3pv4w-3000.app.github.dev"

# Obtener localidades
async def obtener_localidades():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/localidades")
        return response.json()

# Obtener barrios por localidad
async def obtener_barrios(id_localidad: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/barrios/{id_localidad}")
        return response.json()