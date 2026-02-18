from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import router as login_router  # Importa el router de login
import os

app = FastAPI()

# Configurar CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(login_router)

# Servir archivos estáticos (para el frontend)
# Si tienes una carpeta "static" con tu HTML y JS
# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {
        "mensaje": "API funcionando correctamente",
        "endpoints": {
            "login": "POST /login",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/health")
async def health_check():
    """Endpoint para verificar que la API está funcionando"""
    return {
        "status": "healthy",
        "database_url": "configurada" if os.getenv("DATABASE_URL") else "no configurada"
    }
