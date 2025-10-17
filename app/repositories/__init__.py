"""
Paquete de repositorios para operaciones CRUD.

Este paquete contiene todos los repositorios que manejan
las operaciones de base de datos para cada modelo.
"""

from .articulo_repository import ArticuloRepository
from .persona_repository import PersonaRepository
from .reserva_repository import ReservaRepository
from .sala_repository import SalaRepository

__all__ = [
    "PersonaRepository",
    "ArticuloRepository",
    "SalaRepository",
    "ReservaRepository",
]
