"""
Esquemas Pydantic del Sistema de Reservas.

Este paquete contiene todos los esquemas de validación y serialización
para las operaciones de la API REST.
"""

# Importar todos los esquemas
from .persona import Persona, PersonaCreate, PersonaUpdate
from .articulo import Articulo, ArticuloCreate, ArticuloUpdate
from .sala import Sala, SalaCreate, SalaUpdate
from .reserva import Reserva, ReservaCreate, ReservaUpdate

# Exportar todos los esquemas
__all__ = [
    "Persona", "PersonaCreate", "PersonaUpdate",
    "Articulo", "ArticuloCreate", "ArticuloUpdate",
    "Sala", "SalaCreate", "SalaUpdate",
    "Reserva", "ReservaCreate", "ReservaUpdate"
    ]