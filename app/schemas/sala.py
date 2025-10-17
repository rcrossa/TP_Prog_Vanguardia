"""
Esquemas Pydantic para el modelo Sala.

Este módulo define los esquemas de validación y serialización
para las operaciones CRUD del modelo Sala.
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SalaBase(BaseModel):
    """Esquema base para salas con campos comunes."""

    nombre: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre identificativo de la sala",
        examples=[
            "Sala de Conferencias A",
            "Aula Magna",
            "Sala de Juntas 101",
            "Laboratorio de Computación",
        ],
    )
    capacidad: int = Field(
        ...,
        gt=0,
        le=1000,
        description="Capacidad máxima de personas que puede albergar la sala",
        examples=[10, 25, 50, 100, 300],
    )


class SalaCreate(SalaBase):
    """
    Esquema para crear una nueva sala.

    La capacidad debe ser un número positivo que represente
    la cantidad máxima de personas que pueden usar la sala simultáneamente.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"nombre": "Sala de Reuniones Executive", "capacidad": 12}
        }
    )


class SalaUpdate(BaseModel):
    """
    Esquema para actualizar una sala existente.

    Permite modificar tanto el nombre como la capacidad.
    Útil para actualizaciones de configuración o remodelaciones.
    """

    nombre: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="Nuevo nombre de la sala",
        examples=["Sala Renovada 2024", "Aula Tecnológica Premium"],
    )
    capacidad: Optional[int] = Field(
        None,
        gt=0,
        le=1000,
        description="Nueva capacidad máxima de la sala",
        examples=[15, 30, 75, 150],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"nombre": "Sala de Conferencias Renovada", "capacidad": 20}
        }
    )


class Sala(SalaBase):
    """
    Esquema completo de sala con ID para respuestas de la API.

    Incluye el identificador único y toda la información
    de configuración de la sala.
    """

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {"id": 1, "nombre": "Sala de Conferencias A", "capacidad": 25}
        },
    )

    id: int = Field(
        ..., description="Identificador único de la sala", examples=[1, 2, 3, 42, 100]
    )
