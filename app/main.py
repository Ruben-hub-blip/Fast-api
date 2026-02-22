from fastapi import FastAPI
from app.routes import (
    roles_routes,
    modulos_routes,
    rol_modulo_routes,
    usuarios_routes,
    reportes_routes,
    fotos_routes,
    comentarios_routes,
    historial_routes
)

app = FastAPI(title="API Reportes Comunidad")

app.include_router(roles_routes.router)
app.include_router(modulos_routes.router)
app.include_router(rol_modulo_routes.router)
app.include_router(usuarios_routes.router)
app.include_router(reportes_routes.router)
app.include_router(fotos_routes.router)
app.include_router(comentarios_routes.router)
app.include_router(historial_routes.router)
