"""
Paquete de la API REST.

Este paquete contiene todas las versiones
de la API REST del sistema.
"""

from .v1 import api_router

__all__ = ["api_router"]
