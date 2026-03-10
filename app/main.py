from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.usuarios_routes import router as usuarios_router
from app.routes.roles_routes import router as roles_router
from app.routes.modulos_routes import router as modulos_router
from app.routes.rol_modulo_routes import router as rol_modulo_router
from app.routes.reportes_routes import router as reportes_router
from app.routes.comentarios_routes import router as comentarios_router
from app.routes.fotos_routes import router as fotos_router
from app.routes.historial_routes import router as historial_router
from app.routes.auth_routes import router as auth_router
from app.routes import ubicaciones_routes
from app.config.db_config import get_connection
from app.routes import barrios


app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, tags=["Auth"])
app.include_router(usuarios_router)
app.include_router(roles_router)
app.include_router(modulos_router)
app.include_router(rol_modulo_router)
app.include_router(reportes_router)
app.include_router(ubicaciones_routes.router)
app.include_router(comentarios_router)
app.include_router(fotos_router)
app.include_router(historial_router)
app.include_router(barrios.router, prefix="/ubicaciones")


@app.get("/")
def read_root():
    return {"mensaje": "API funcionando correctamente"}


