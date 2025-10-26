
"""
Esquemas Pydantic para el modelo Persona.

Este módulo define los esquemas de validación y serialización
para las operaciones CRUD del modelo Persona.
"""
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class PersonaBase(BaseModel):
    """Esquema base para personas con campos comunes."""

    nombre: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre completo de la persona",
        examples=["Juan Pérez", "María González", "Carlos Rodríguez"],
    )
    email: EmailStr = Field(
        ...,
        description="Dirección de email válida y única",
        examples=[
            "juan.perez@email.com",
            "maria.gonzalez@universidad.edu",
            "carlos@empresa.com",
        ],
    )


class PersonaCreate(PersonaBase):
    """
    Esquema para crear una nueva persona.

    Valida que el nombre no esté vacío y que el email tenga formato válido.
    El email debe ser único en todo el sistema.
    Incluye campos para contraseña y perfil de administrador.
    """

    password: str = Field(
        ...,
        min_length=6,
        max_length=128,
        description="Contraseña del usuario (mínimo 6 caracteres)",
        examples=["admin123", "user123", "securepassword"],
    )
    is_admin: bool = Field(
        default=False,
        description="Si el usuario tiene permisos de administrador",
        examples=[True, False],
    )
    is_active: bool = Field(
        default=True,
        description="Si el usuario está activo en el sistema",
        examples=[True, False],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Ana Martínez",
                "email": "ana.martinez@email.com",
                "password": "admin123",
                "is_admin": True,
                "is_active": True,
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
        examples=["Juan Carlos Pérez", "María José González"],
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Nueva dirección de email (debe ser única)",
        examples=["nuevo.email@email.com", "actualizado@empresa.com"],
    )
    password: Optional[str] = Field(
        None,
        min_length=6,
        max_length=128,
        description="Nueva contraseña del usuario (mínimo 6 caracteres)",
        examples=["newpassword123", "securepassword"],
    )
    is_admin: Optional[bool] = Field(
        None, description="Nuevos permisos de administrador", examples=[True, False]
    )
    is_active: Optional[bool] = Field(
        None, description="Nuevo estado del usuario", examples=[True, False]
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Juan Carlos Pérez",
                "email": "juan.carlos@newemail.com",
                "password": "newpassword123",
                "is_admin": False,
                "is_active": True,
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
                "email": "juan.perez@email.com",
                "is_admin": False,
                "is_active": True,
            }
        },
    )

    id: int = Field(
        ...,
        description="Identificador único de la persona",
        examples=[1, 2, 3, 42, 100],
    )
    is_admin: bool = Field(
        ...,
        description="Si el usuario tiene permisos de administrador",
        examples=[True, False],
    )
    is_active: bool = Field(
        ...,
        description="Si el usuario está activo en el sistema",
        examples=[True, False],
    )


class PersonaLogin(BaseModel):
    """Esquema para el login de usuarios."""

    email: EmailStr = Field(
        ...,
        description="Email del usuario",
        examples=["admin@test.com", "user@test.com"],
    )
    password: str = Field(
        ...,
        min_length=1,
        description="Contraseña del usuario",
        examples=["admin123", "user123"],
    )


class PersonaLoginResponse(BaseModel):
    """Esquema para la respuesta del login."""

    access_token: str = Field(
        ...,
        description="Token JWT para autenticación",
        examples=["eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."],
    )
    token_type: str = Field(
        default="bearer", description="Tipo de token", examples=["bearer"]
    )
    user: Persona = Field(..., description="Datos del usuario autenticado")
