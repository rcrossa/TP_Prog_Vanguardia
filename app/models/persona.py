
"""
Modelo de datos para personas/usuarios del sistema.

Este módulo define el modelo Persona que representa a los usuarios
que pueden realizar reservas en el sistema.
"""
from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base
if TYPE_CHECKING:
    from app.models.reserva import Reserva


class Persona(Base):
    """
    Modelo de persona/usuario del sistema.

    Representa a los usuarios que pueden realizar reservas en el sistema.
    Cada persona tiene un email único y puede tener múltiples reservas asociadas.
    Incluye campos de autenticación para login del sistema.
    """

    __tablename__ = "personas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    apellido: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    # Campos de autenticación
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relación con reservas
    reservas: Mapped[List[Reserva]] = relationship(back_populates="persona")

    def __repr__(self):
        return f"<Persona(id={self.id}, nombre='{self.nombre}', email='{self.email}'," \
               f" is_active={self.is_active})>"

    def has_password(self) -> bool:
        """Verificar si el usuario tiene una contraseña configurada."""
        return self.hashed_password is not None

    def is_authenticated(self) -> bool:
        """Verificar si el usuario puede autenticarse."""
        return self.is_active and self.has_password()
