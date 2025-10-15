"""
Modelos de datos del Sistema de Reservas.

Este paquete contiene todos los modelos SQLAlchemy que representan
las entidades del sistema: Persona, Articulo, Sala y Reserva.
"""

# Importar todos los modelos para facilitar el acceso
from .persona import Persona
from .articulo import Articulo
from .sala import Sala
from .reserva import Reserva

# Exportar todos los modelos
__all__ = ["Persona", "Articulo", "Sala", "Reserva"]