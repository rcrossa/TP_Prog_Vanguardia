"""
Paquete de endpoints de la API v1.

Este paquete contiene todos los routers de endpoints
para los diferentes modelos del sistema.
"""

from .articulos import router as articulos_router
from .personas import router as personas_router
from .reservas import router as reservas_router
from .salas import router as salas_router

__all__ = ["personas_router", "articulos_router", "salas_router", "reservas_router"]
