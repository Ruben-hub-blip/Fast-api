import httpx

EXPRESS_API = "https://super-spork-x5vxjr65w4vj3pv4w-3000.app.github.dev"


async def obtener_localidades():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{EXPRESS_API}/localidades")
        return response.json()


async def obtener_barrios():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{EXPRESS_API}/barrios")
        return response.json()