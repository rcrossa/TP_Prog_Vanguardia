
"""
Router principal de la API v1.

Este módulo configura todos los routers de endpoints
y los agrupa bajo el prefijo /api/v1.
"""
from fastapi import APIRouter
from app.api.v1.endpoints import (
    articulos_router,
    personas_router,
    reservas_router,
    salas_router,
)
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.integration import router as integration_router

api_router = APIRouter()

# Incluir todos los routers de endpoints
api_router.include_router(auth_router)
api_router.include_router(personas_router)
api_router.include_router(articulos_router)
api_router.include_router(salas_router)
api_router.include_router(reservas_router)
api_router.include_router(integration_router, tags=["🔗 Integration"])
