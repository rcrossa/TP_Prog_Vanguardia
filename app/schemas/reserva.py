"""
Esquemas Pydantic para el modelo Reserva.

Este módulo define los esquemas de validación y serialización
para las operaciones CRUD del modelo Reserva.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ReservaBase(BaseModel):
    """Esquema base para reservas con campos comunes."""

    id_persona: int = Field(
        ...,
        gt=0,
        description="ID de la persona que realiza la reserva",
        examples=[1, 2, 3, 42],
    )
    fecha_hora_inicio: datetime = Field(
        ...,
        description="Fecha y hora de inicio de la reserva (formato ISO 8601)",
        examples=["2025-10-16T09:00:00", "2025-10-17T14:30:00", "2025-10-18T08:00:00"],
    )
    fecha_hora_fin: datetime = Field(
        ...,
        description="Fecha y hora de fin de la reserva (formato ISO 8601)",
        examples=["2025-10-16T10:00:00", "2025-10-17T16:30:00", "2025-10-18T10:00:00"],
    )
    id_articulo: Optional[int] = Field(
        None,
        gt=0,
        description="ID del artículo a reservar (exclusivo con id_sala)",
        examples=[1, 2, 3, None],
    )
    id_sala: Optional[int] = Field(
        None,
        gt=0,
        description="ID de la sala a reservar (exclusivo con id_articulo)",
        examples=[1, 2, 3, None],
    )

    @field_validator("fecha_hora_fin")
    @classmethod
    def validate_fecha_fin(cls, v: datetime, info) -> datetime:
        """Validar que la fecha de fin sea posterior a la fecha de inicio."""
        fecha_inicio = info.data.get("fecha_hora_inicio")
        if fecha_inicio and v <= fecha_inicio:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")
        return v


class ReservaCreate(ReservaBase):
    """
    Esquema para crear una nueva reserva.

    ### 🚨 Reglas Importantes
    - Una reserva debe ser para UN artículo O UNA sala (no ambos, no ninguno)
    - La fecha de fin debe ser posterior a la fecha de inicio
    - No se pueden crear reservas en el pasado
    - El sistema detecta automáticamente conflictos de horarios

    ### 📋 Validaciones Automáticas
    - Verifica que la persona existe
    - Valida disponibilidad del artículo (si aplica)
    - Detecta conflictos de horario en salas (si aplica)
    - Valida que las fechas sean lógicas
    """

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "description": "Reserva de artículo",
                    "value": {
                        "id_persona": 1,
                        "fecha_hora_inicio": "2025-10-16T09:00:00",
                        "fecha_hora_fin": "2025-10-16T17:00:00",
                        "id_articulo": 1,
                        "id_sala": None,
                    },
                },
                {
                    "description": "Reserva de sala",
                    "value": {
                        "id_persona": 2,
                        "fecha_hora_inicio": "2025-10-17T14:00:00",
                        "fecha_hora_fin": "2025-10-17T16:00:00",
                        "id_articulo": None,
                        "id_sala": 1,
                    },
                },
            ]
        }
    )


class ReservaUpdate(BaseModel):
    """
    Esquema para actualizar una reserva existente.

    Permite modificar cualquier aspecto de la reserva.
    Las mismas validaciones de creación se aplican a las actualizaciones.
    """

    id_persona: Optional[int] = Field(
        None, gt=0, description="Nuevo ID de la persona responsable", examples=[1, 2, 3]
    )
    fecha_hora_inicio: Optional[datetime] = Field(
        None,
        description="Nueva fecha y hora de inicio",
        examples=["2025-10-16T10:00:00", "2025-10-17T15:00:00"],
    )
    fecha_hora_fin: Optional[datetime] = Field(
        None,
        description="Nueva fecha y hora de fin",
        examples=["2025-10-16T12:00:00", "2025-10-17T17:00:00"],
    )
    id_articulo: Optional[int] = Field(
        None,
        gt=0,
        description="Nuevo ID del artículo (usar null para limpiar)",
        examples=[1, 2, 3, None],
    )
    id_sala: Optional[int] = Field(
        None,
        gt=0,
        description="Nuevo ID de la sala (usar null para limpiar)",
        examples=[1, 2, 3, None],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "fecha_hora_inicio": "2025-10-16T10:00:00",
                "fecha_hora_fin": "2025-10-16T12:00:00",
            }
        }
    )


class Reserva(ReservaBase):
    """
    Esquema completo de reserva con ID para respuestas de la API.

    Incluye el identificador único y toda la información de la reserva.
    Las respuestas pueden incluir las relaciones expandidas (persona, sala, artículo).
    """

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "description": "Reserva de artículo",
                    "value": {
                        "id": 1,
                        "id_persona": 1,
                        "fecha_hora_inicio": "2025-10-16T09:00:00",
                        "fecha_hora_fin": "2025-10-16T17:00:00",
                        "id_articulo": 1,
                        "id_sala": None,
                    },
                },
                {
                    "description": "Reserva de sala",
                    "value": {
                        "id": 2,
                        "id_persona": 2,
                        "fecha_hora_inicio": "2025-10-17T14:00:00",
                        "fecha_hora_fin": "2025-10-17T16:00:00",
                        "id_articulo": None,
                        "id_sala": 1,
                    },
                },
            ]
        },
    )

    id: int = Field(
        ...,
        description="Identificador único de la reserva",
        examples=[1, 2, 3, 42, 100],
    )
