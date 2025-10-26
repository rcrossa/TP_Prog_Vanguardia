"""auth"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
# Constantes para valores repetidos

MIN_PASSWORD_LENGTH = 6
TOKEN_EXPIRES_IN = 1800
# Constantes para ejemplos
EXAMPLE_EMAIL = "juan@ejemplo.com"
EXAMPLE_USER_EMAIL = "usuario@ejemplo.com"
EXAMPLE_NOMBRE = "Juan Pérez"
EXAMPLE_PASSWORD = "micontraseña123"
"""
Esquemas Pydantic para autenticación y autorización.

Este módulo define los esquemas para login, registro, tokens
y respuestas de autenticación.
"""

class UserLogin(BaseModel):
    """Esquema para login de usuario."""

    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., min_length=MIN_PASSWORD_LENGTH,
                          description=f"Contraseña del usuario "
                          f"(mínimo {MIN_PASSWORD_LENGTH} caracteres)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"email": EXAMPLE_USER_EMAIL, "password": EXAMPLE_PASSWORD}
        }
    )


class UserRegister(BaseModel):
    """Esquema para registro de nuevo usuario."""

    nombre: str = Field(
        ..., min_length=2, max_length=255, description="Nombre completo"
    )
    email: EmailStr = Field(..., description="Email único del usuario")
    password: str = Field(
        ..., min_length=MIN_PASSWORD_LENGTH,
        description=f"Contraseña (mínimo {MIN_PASSWORD_LENGTH} caracteres)"
    )
    confirm_password: str = Field(..., description="Confirmación de contraseña")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": EXAMPLE_NOMBRE,
                "email": EXAMPLE_EMAIL,
                "password": EXAMPLE_PASSWORD,
                "confirm_password": EXAMPLE_PASSWORD,
            }
        }
    )

    def passwords_match(self) -> bool:
        """Verificar que las contraseñas coincidan."""
        return self.password == self.confirm_password


class UserChangePassword(BaseModel):
    """Esquema para cambio de contraseña."""

    current_password: str = Field(..., description="Contraseña actual")
    new_password: str = Field(..., min_length=MIN_PASSWORD_LENGTH,
                              description=f"Nueva contraseña (mínimo "
                              f"{MIN_PASSWORD_LENGTH} caracteres)")
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
                "expires_in": TOKEN_EXPIRES_IN,
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
                "nombre": EXAMPLE_NOMBRE,
                "email": EXAMPLE_EMAIL,
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
                    "nombre": EXAMPLE_NOMBRE,
                    "email": EXAMPLE_EMAIL,
                    "is_active": True,
                    "is_admin": False,
                    "has_password": True,
                },
                "token": {
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    "token_type": "bearer",
                    "expires_in": TOKEN_EXPIRES_IN,
                },
            }
        }
    )
