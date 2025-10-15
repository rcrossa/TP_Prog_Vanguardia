"""
Paquete de repositorios para operaciones CRUD.

Este paquete contiene todos los repositorios que manejan
las operaciones de base de datos para cada modelo.
"""

from .persona_repository import PersonaRepository
from .articulo_repository import ArticuloRepository
from .sala_repository import SalaRepository
from .reserva_repository import ReservaRepository

__all__ = [
    "PersonaRepository",
    "ArticuloRepository", 
    "SalaRepository",
    "ReservaRepository"
]
