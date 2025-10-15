"""
Modelo de datos para artículos reservables.

Este módulo define el modelo Articulo que representa los recursos físicos
que pueden ser reservados en el sistema (proyectores, laptops, etc.).
"""

from __future__ import annotations
from typing import List, TYPE_CHECKING
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.reserva import Reserva


class Articulo(Base):
    """
    Modelo de artículo reservable.

    Representa recursos físicos que pueden ser reservados como proyectores,
    laptops, cámaras, etc. Cada artículo tiene un estado de disponibilidad
    y puede tener múltiples reservas asociadas.
    """
    __tablename__ = "articulos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    disponible: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # Relación con reservas
    reservas: Mapped[List[Reserva]] = relationship(back_populates="articulo")

    def __repr__(self):
        return f"<Articulo(id={self.id}, nombre='{self.nombre}', disponible={self.disponible})>"