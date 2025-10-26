
"""
Modelo de datos para salas reservables.

Este módulo define el modelo Sala que representa los espacios físicos
que pueden ser reservados en el sistema (salas de reunión, aulas, etc.).
"""
from __future__ import annotations
from typing import TYPE_CHECKING, List
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
if TYPE_CHECKING:
    from app.models.reserva import Reserva


class Sala(Base):
    """
    Modelo de sala reservable.

    Representa espacios físicos que pueden ser reservados como salas de reunión,
    aulas, laboratorios, etc. Cada sala tiene una capacidad máxima y puede tener
    múltiples reservas asociadas.
    """

    __tablename__ = "salas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    capacidad: Mapped[int] = mapped_column(Integer, nullable=False)
    disponible: Mapped[bool] = mapped_column(nullable=False, default=True)
    ubicacion: Mapped[str] = mapped_column(String(255), nullable=True, default="")
    descripcion: Mapped[str] = mapped_column(String(255), nullable=True, default="")

    # Relación con reservas
    reservas: Mapped[List[Reserva]] = relationship(back_populates="sala")

    def __repr__(self):
        return (
            f"<Sala(id={self.id}, nombre='{self.nombre}', capacidad={self.capacidad})>"
        )
