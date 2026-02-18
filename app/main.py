from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.user_routes import router as user_router
import os

@app.get("/test-env")
def test_env():
    return {
        "database_url": str(os.getenv("DATABASE_URL"))[:30]
    }

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)

@app.get("/")
def read_root():
    return {"mensaje": "API funcionando correctamente"}


