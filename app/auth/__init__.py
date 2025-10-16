"""
Módulo de autenticación y autorización.

Este paquete contiene todo lo relacionado con la autenticación JWT,
manejo de contraseñas, dependencias de seguridad y utilidades de auth.
"""

from .jwt_handler import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token,
    extract_email_from_token
)
from .dependencies import (
    get_current_user,
    get_current_active_user,
    get_current_admin_user,
    get_optional_current_user
)

__all__ = [
    "verify_password",
    "get_password_hash", 
    "create_access_token",
    "verify_token",
    "extract_email_from_token",
    "get_current_user",
    "get_current_active_user",
    "get_current_admin_user",
    "get_optional_current_user"
]