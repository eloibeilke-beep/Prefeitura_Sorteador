from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
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

# Configuração para servir os arquivos do Frontend e App Mobile
current_dir = os.path.dirname(os.path.realpath(__file__))
# Sobe dois níveis para chegar na raiz do projeto 'SORTEIO ONLINE'
root_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))

app.mount("/app-mobile", StaticFiles(directory=os.path.join(root_dir, "app-mobile")), name="app-mobile")
app.mount("/frontend-admin", StaticFiles(directory=os.path.join(root_dir, "frontend-admin")), name="frontend-admin")

@app.get("/")
def home():
    return {"status": "ok"}