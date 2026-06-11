from fastapi import APIRouter
from .notas import router as notas_router
from .usuarios import router as usuarios_router
from .sorteios import router as sorteios_router

api_router = APIRouter()

api_router.include_router(notas_router)
api_router.include_router(usuarios_router)
api_router.include_router(sorteios_router)
