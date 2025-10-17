"""
Modelos de datos del Sistema de Reservas.

Este paquete contiene todos los modelos SQLAlchemy que representan
las entidades del sistema: Persona, Articulo, Sala y Reserva.
"""

from .articulo import Articulo

# Importar todos los modelos para facilitar el acceso
from .persona import Persona
from .reserva import Reserva
from .sala import Sala

# Exportar todos los modelos
__all__ = ["Persona", "Articulo", "Sala", "Reserva"]
