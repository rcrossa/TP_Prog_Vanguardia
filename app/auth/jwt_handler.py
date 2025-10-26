"""
Sistema de autenticación JWT para el Sistema de Reservas.

Este módulo contiene las utilidades para generar y verificar tokens JWT,
hashear contraseñas y manejar la autenticación de usuarios.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Configuración para hashear contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración JWT
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verificar que una contraseña plana coincida con su hash.

    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Contraseña hasheada

    Returns:
        True si coinciden, False si no
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generar hash seguro de una contraseña.

    Args:
        password: Contraseña en texto plano

    Returns:
        Hash seguro de la contraseña
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crear token JWT de acceso.

    Args:
        data: Datos a incluir en el token (normalmente user_id, email)
        expires_delta: Tiempo de expiración personalizado

    Returns:
        Token JWT codificado
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verificar y decodificar un token JWT.

    Args:
        token: Token JWT a verificar

    Returns:
        Payload del token si es válido, None si es inválido
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def extract_email_from_token(token: str) -> Optional[str]:
    """
    Extraer email del payload de un token JWT.

    Args:
        token: Token JWT

    Returns:
        Email del usuario si el token es válido, None si no
    """
    payload = verify_token(token)
    if payload:
        return payload.get("sub")
    return None
