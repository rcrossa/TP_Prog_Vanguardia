"""
Esquemas Pydantic para autenticación y autorización.

Este módulo define los esquemas para login, registro, tokens
y respuestas de autenticación.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserLogin(BaseModel):
    """Esquema para login de usuario."""

    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., min_length=6, description="Contraseña del usuario")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"email": "usuario@ejemplo.com", "password": "micontraseña123"}
        }
    )


class UserRegister(BaseModel):
    """Esquema para registro de nuevo usuario."""

    nombre: str = Field(
        ..., min_length=2, max_length=255, description="Nombre completo"
    )
    email: EmailStr = Field(..., description="Email único del usuario")
    password: str = Field(
        ..., min_length=6, description="Contraseña (mínimo 6 caracteres)"
    )
    confirm_password: str = Field(..., description="Confirmación de contraseña")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Juan Pérez",
                "email": "juan@ejemplo.com",
                "password": "micontraseña123",
                "confirm_password": "micontraseña123",
            }
        }
    )

    def passwords_match(self) -> bool:
        """Verificar que las contraseñas coincidan."""
        return self.password == self.confirm_password


class UserChangePassword(BaseModel):
    """Esquema para cambio de contraseña."""

    current_password: str = Field(..., description="Contraseña actual")
    new_password: str = Field(..., min_length=6, description="Nueva contraseña")
    confirm_new_password: str = Field(
        ..., description="Confirmación de nueva contraseña"
    )

    def passwords_match(self) -> bool:
        """Verificar que las nuevas contraseñas coincidan."""
        return self.new_password == self.confirm_new_password


class Token(BaseModel):
    """Esquema para respuesta de token JWT."""

    access_token: str = Field(..., description="Token JWT de acceso")
    token_type: str = Field(default="bearer", description="Tipo de token")
    expires_in: int = Field(..., description="Tiempo de expiración en segundos")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
            }
        }
    )


class TokenData(BaseModel):
    """Esquema para datos dentro del token."""

    email: Optional[str] = None


class UserProfile(BaseModel):
    """Esquema para perfil de usuario autenticado."""

    id: int = Field(..., description="ID único del usuario")
    nombre: str = Field(..., description="Nombre completo")
    email: EmailStr = Field(..., description="Email del usuario")
    is_active: bool = Field(..., description="Usuario activo")
    is_admin: bool = Field(..., description="Usuario administrador")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    last_login: Optional[datetime] = Field(None, description="Último login")
    has_password: bool = Field(..., description="Tiene contraseña configurada")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "nombre": "Juan Pérez",
                "email": "juan@ejemplo.com",
                "is_active": True,
                "is_admin": False,
                "created_at": "2025-10-15T21:00:00",
                "last_login": "2025-10-15T21:30:00",
                "has_password": True,
            }
        },
    )


class LoginResponse(BaseModel):
    """Respuesta completa del login."""

    message: str = Field(..., description="Mensaje de éxito")
    user: UserProfile = Field(..., description="Datos del usuario")
    token: Token = Field(..., description="Token de acceso")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Login exitoso",
                "user": {
                    "id": 1,
                    "nombre": "Juan Pérez",
                    "email": "juan@ejemplo.com",
                    "is_active": True,
                    "is_admin": False,
                    "has_password": True,
                },
                "token": {
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    "token_type": "bearer",
                    "expires_in": 1800,
                },
            }
        }
    )
