"""
Modelo de datos para personas/usuarios del sistema.

Este módulo define el modelo Persona que representa a los usuarios
que pueden realizar reservas en el sistema.
"""

from __future__ import annotations
from typing import List, TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.reserva import Reserva


class Persona(Base):
    """
    Modelo de persona/usuario del sistema.

    Representa a los usuarios que pueden realizar reservas en el sistema.
    Cada persona tiene un email único y puede tener múltiples reservas asociadas.
    """
    __tablename__ = "personas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    # Relación con reservas
    reservas: Mapped[List[Reserva]] = relationship(back_populates="persona")

    def __repr__(self):
        return f"<Persona(id={self.id}, nombre='{self.nombre}', email='{self.email}')>"