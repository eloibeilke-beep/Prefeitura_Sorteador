from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.notas import router as notas_router
from .routes.usuarios import router as usuarios_router
from .routes.sorteios import router as sorteios_router
from .database import engine, Base
from . import models

# Cria as tabelas no banco de dados (SQLite ou Postgres) ao iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Iporã Premiada")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notas_router)
app.include_router(usuarios_router)
app.include_router(sorteios_router)

@app.get("/")
def home():
    return {"status": "ok"}