from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router  # Importa SOLO de routes/__init__.py

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)  # Incluye el router

@app.get("/")
def read_root():
    return {
        "mensaje": "API funcionando correctamente",
        "endpoints": {
            "login": "POST /login",
            "login_test": "GET /login-test",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database_url": "configurada"}
