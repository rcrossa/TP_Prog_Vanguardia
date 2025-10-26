
"""
Modelo de datos para reservas del sistema.

Este módulo define el modelo Reserva que representa las reservas
realizadas por personas para artículos o salas específicas.
"""
from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
if TYPE_CHECKING:
    from app.models.articulo import Articulo
    from app.models.persona import Persona
    from app.models.sala import Sala


class Reserva(Base):
    """
    Modelo de reserva del sistema.

    Representa una reserva realizada por una persona para un artículo o sala
    específica en un período de tiempo determinado. Una reserva debe tener
    una persona asociada y puede ser para un artículo O una sala (no ambos).
    """

    __tablename__ = "reservas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_articulo: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("articulos.id"), nullable=True
    )
    id_sala: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("salas.id"), nullable=True
    )
    id_persona: Mapped[int] = mapped_column(
        Integer, ForeignKey("personas.id"), nullable=False
    )
    fecha_hora_inicio: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fecha_hora_fin: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Relaciones
    persona: Mapped[Persona] = relationship(back_populates="reservas")
    articulo: Mapped[Optional[Articulo]] = relationship(back_populates="reservas")
    sala: Mapped[Optional[Sala]] = relationship(back_populates="reservas")

    def __repr__(self):
        return (
            f"<Reserva(id={self.id}, id_persona={self.id_persona}, "
            f"id_articulo={self.id_articulo}, id_sala={self.id_sala}, "
            f"inicio='{self.fecha_hora_inicio}', fin='{self.fecha_hora_fin}')>"
        )
