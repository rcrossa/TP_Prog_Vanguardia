"""
Router principal de la API v1.

Este módulo configura todos los routers de endpoints
y los agrupa bajo el prefijo /api/v1.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import (
    personas_router,
    articulos_router,
    salas_router,
    reservas_router
)
from app.api.v1.endpoints.demo import router as demo_router

api_router = APIRouter()

# Incluir todos los routers de endpoints
api_router.include_router(personas_router)
api_router.include_router(articulos_router)
api_router.include_router(salas_router)
api_router.include_router(reservas_router)
api_router.include_router(demo_router)