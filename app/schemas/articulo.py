"""
Esquemas Pydantic para el modelo Articulo.

Este módulo define los esquemas de validación y serialización
para las operaciones CRUD del modelo Articulo.
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ArticuloBase(BaseModel):
    """Esquema base para artículos con campos comunes."""

    nombre: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre descriptivo del artículo",
        examples=[
            "Laptop Dell XPS 13",
            "Proyector Epson",
            "Mesa de Reuniones",
            "Libro: Python Programming",
        ],
    )
    descripcion: Optional[str] = Field(
        None,
        max_length=500,
        description="Descripción detallada del artículo",
        examples=["Laptop de alta gama para desarrollo"],
    )
    cantidad: int = Field(
        1, ge=0, description="Cantidad disponible del artículo", examples=[1, 5, 10]
    )
    categoria: Optional[str] = Field(
        None,
        max_length=50,
        description="Categoría del artículo",
        examples=["Informática", "Electrónica", "Mobiliario"],
    )
    disponible: bool = Field(
        True,
        description="Estado de disponibilidad del artículo para reservas",
        examples=[True, False],
    )


class ArticuloCreate(ArticuloBase):
    """
    Esquema para crear un nuevo artículo.

    Por defecto, los artículos se crean como disponibles con cantidad 1.
    El nombre debe ser descriptivo y único para evitar confusiones.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "MacBook Pro 16 pulgadas",
                "descripcion": "Laptop de alta gama para desarrollo",
                "cantidad": 3,
                "categoria": "Informática",
                "disponible": True,
            }
        }
    )


class ArticuloUpdate(BaseModel):
    """
    Esquema para actualizar un artículo existente.

    Permite modificar tanto el nombre como el estado de disponibilidad.
    Todos los campos son opcionales.
    """

    nombre: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="Nuevo nombre del artículo",
        examples=["Laptop Dell XPS 15 Actualizada", "Proyector 4K Nuevo"],
    )
    disponible: Optional[bool] = Field(
        None, description="Nuevo estado de disponibilidad", examples=[True, False]
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"nombre": "iPad Pro 12.9 pulgadas", "disponible": False}
        }
    )


class Articulo(ArticuloBase):
    """
    Esquema completo de artículo con ID para respuestas de la API.

    Incluye el identificador único asignado automáticamente
    junto con toda la información del artículo.
    """

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "nombre": "MacBook Pro 16 pulgadas",
                "disponible": True,
            }
        },
    )

    id: int = Field(
        ..., description="Identificador único del artículo", examples=[1, 2, 3, 42, 100]
    )
