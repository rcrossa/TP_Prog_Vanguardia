"""
Esquemas Pydantic del Sistema de Reservas.

Este paquete contiene todos los esquemas de validación y serialización
para las operaciones de la API REST.
"""

from .articulo import Articulo, ArticuloCreate, ArticuloUpdate

# Importar todos los esquemas
from .persona import Persona, PersonaCreate, PersonaUpdate
from .reserva import Reserva, ReservaCreate, ReservaUpdate
from .sala import Sala, SalaCreate, SalaUpdate

# Exportar todos los esquemas
__all__ = [
    "Persona",
    "PersonaCreate",
    "PersonaUpdate",
    "Articulo",
    "ArticuloCreate",
    "ArticuloUpdate",
    "Sala",
    "SalaCreate",
    "SalaUpdate",
    "Reserva",
    "ReservaCreate",
    "ReservaUpdate",
]
