"""
Dependencias de autenticación para FastAPI.

Este módulo define las dependencias que se pueden usar en los endpoints
para requerir autenticación, verificar permisos, obtener usuario actual, etc.
"""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth.jwt_handler import extract_email_from_token
from app.core.database import get_db
from app.models.persona import Persona
from app.repositories.persona_repository import PersonaRepository

# Configurar el esquema de seguridad Bearer
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> Persona:
    """
    Obtener usuario actual desde el token JWT.

    Args:
        credentials: Credenciales HTTP Bearer
        db: Sesión de base de datos

    Returns:
        Usuario autenticado

    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Extraer email del token
        email = extract_email_from_token(credentials.credentials)
        if email is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    # Buscar usuario por email
    user = PersonaRepository.get_by_email(db, email)
    if user is None:
        raise credentials_exception

    # Verificar que el usuario esté activo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo"
        )

    return user


async def get_current_active_user(
    current_user: Persona = Depends(get_current_user),
) -> Persona:
    """
    Obtener usuario actual activo.

    Args:
        current_user: Usuario actual

    Returns:
        Usuario activo

    Raises:
        HTTPException: Si el usuario está inactivo
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo"
        )
    return current_user


async def get_current_admin_user(
    current_user: Persona = Depends(get_current_active_user),
) -> Persona:
    """
    Obtener usuario administrador actual.

    Args:
        current_user: Usuario actual activo

    Returns:
        Usuario administrador

    Raises:
        HTTPException: Si el usuario no es administrador
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador",
        )
    return current_user


async def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db),
) -> Optional[Persona]:
    """
    Obtener usuario actual opcional (para endpoints que funcionan con o sin auth).

    Args:
        credentials: Credenciales HTTP Bearer opcionales
        db: Sesión de base de datos

    Returns:
        Usuario autenticado o None si no hay token válido
    """
    if not credentials:
        return None

    try:
        email = extract_email_from_token(credentials.credentials)
        if email is None:
            return None

        user = PersonaRepository.get_by_email(db, email)
        if user is None or not user.is_active:
            return None

        return user
    except Exception:
        return None
