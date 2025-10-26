
"""
Modelos de datos del Sistema de Reservas.

Este paquete contiene todos los modelos SQLAlchemy que representan
las entidades del sistema: Persona, Articulo, Sala y Reserva.
"""
from .articulo import Articulo
from .persona import Persona
from .reserva import Reserva
from .sala import Sala
__all__ = ["Persona", "Articulo", "Sala", "Reserva"]
