"""
Esquemas Pydantic para el modelo Persona.

Este módulo define los esquemas de validación y serialización
para las operaciones CRUD del modelo Persona.
"""

from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional


class PersonaBase(BaseModel):
    """Esquema base para personas con campos comunes."""
    nombre: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre completo de la persona",
        examples=["Juan Pérez", "María González", "Carlos Rodríguez"]
    )
    email: EmailStr = Field(
        ...,
        description="Dirección de email válida y única",
        examples=["juan.perez@email.com", "maria.gonzalez@universidad.edu", "carlos@empresa.com"]
    )


class PersonaCreate(PersonaBase):
    """
    Esquema para crear una nueva persona.
    
    Valida que el nombre no esté vacío y que el email tenga formato válido.
    El email debe ser único en todo el sistema.
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Ana Martínez",
                "email": "ana.martinez@email.com"
            }
        }
    )


class PersonaUpdate(BaseModel):
    """
    Esquema para actualizar una persona existente.
    
    Todos los campos son opcionales. Solo se actualizarán
    los campos proporcionados en la petición.
    """
    nombre: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="Nuevo nombre de la persona",
        examples=["Juan Carlos Pérez", "María José González"]
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Nueva dirección de email (debe ser única)",
        examples=["nuevo.email@email.com", "actualizado@empresa.com"]
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Juan Carlos Pérez",
                "email": "juan.carlos@newemail.com"
            }
        }
    )


class Persona(PersonaBase):
    """
    Esquema completo de persona con ID para respuestas de la API.
    
    Incluye todos los campos de la persona más el ID único
    asignado automáticamente por el sistema.
    """
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "nombre": "Juan Pérez",
                "email": "juan.perez@email.com"
            }
        }
    )

    id: int = Field(
        ...,
        description="Identificador único de la persona",
        examples=[1, 2, 3, 42, 100]
    )