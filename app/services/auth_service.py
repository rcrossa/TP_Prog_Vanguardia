"""
Servicio de autenticación para el Sistema de Reservas.

Este módulo contiene la lógica de negocio para autenticación,
login, registro y gestión de usuarios.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.jwt_handler import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.models.persona import Persona
from app.repositories.persona_repository import PersonaRepository
from app.schemas.auth import (
    Token,
    UserChangePassword,
    UserLogin,
    UserProfile,
    UserRegister,
)


class AuthService:
    """Servicio para operaciones de autenticación."""

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[Persona]:
        """
        Autenticar usuario con email y contraseña.

        Args:
            db: Sesión de base de datos
            email: Email del usuario
            password: Contraseña en texto plano

        Returns:
            Usuario autenticado o None si falla la autenticación
        """
        user = PersonaRepository.get_by_email(db, email)

        if not user:
            return None

        if not user.hashed_password:
            return None

        if not user.is_active:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    @staticmethod
    def login_user(db: Session, login_data: UserLogin) -> dict:
        """
        Realizar login de usuario y generar token.

        Args:
            db: Sesión de base de datos
            login_data: Datos de login

        Returns:
            Diccionario con usuario y token

        Raises:
            HTTPException: Si las credenciales son inválidas
        """
        user = AuthService.authenticate_user(db, login_data.email, login_data.password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Actualizar último login
        user.last_login = datetime.utcnow()
        db.commit()
        db.refresh(user)

        # Generar token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=access_token_expires,
        )

        # Preparar respuesta
        user_profile = UserProfile(
            id=user.id,
            nombre=user.nombre,
            email=user.email,
            is_active=user.is_active,
            is_admin=user.is_admin,
            created_at=user.created_at,
            last_login=user.last_login,
            has_password=user.has_password(),
        )

        token = Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

        return {"message": "Login exitoso", "user": user_profile, "token": token}

    @staticmethod
    def register_user(db: Session, register_data: UserRegister) -> Persona:
        """
        Registrar nuevo usuario en el sistema.

        Args:
            db: Sesión de base de datos
            register_data: Datos de registro

        Returns:
            Usuario registrado

        Raises:
            HTTPException: Si hay errores de validación
        """
        # Verificar que las contraseñas coincidan
        if not register_data.passwords_match():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Las contraseñas no coinciden",
            )

        # Verificar que el email no exista
        existing_user = PersonaRepository.get_by_email(db, register_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un usuario con el email {register_data.email}",
            )

        # Crear usuario
        hashed_password = get_password_hash(register_data.password)

        user = Persona(
            nombre=register_data.nombre,
            email=register_data.email,
            hashed_password=hashed_password,
            is_active=True,
            is_admin=False,
            created_at=datetime.utcnow(),
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[Persona]:
        """
        Obtener usuario por email.

        Args:
            db: Sesión de base de datos
            email: Email del usuario

        Returns:
            Usuario encontrado o None
        """
        return PersonaRepository.get_by_email(db, email)

    @staticmethod
    def change_password(
        db: Session, user_id: int, password_data: UserChangePassword
    ) -> bool:
        """
        Cambiar contraseña de usuario.

        Args:
            db: Sesión de base de datos
            user_id: ID del usuario
            password_data: Datos de cambio de contraseña

        Returns:
            True si el cambio fue exitoso

        Raises:
            HTTPException: Si hay errores de validación
        """
        user = PersonaRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        # Verificar contraseña actual
        if not user.hashed_password or not verify_password(
            password_data.current_password, user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contraseña actual incorrecta",
            )

        # Verificar que las nuevas contraseñas coincidan
        if not password_data.passwords_match():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Las nuevas contraseñas no coinciden",
            )

        # Cambiar contraseña
        user.hashed_password = get_password_hash(password_data.new_password)
        db.commit()

        return True

    @staticmethod
    def set_user_password(db: Session, user_id: int, password: str) -> bool:
        """
        Establecer contraseña para un usuario que no la tiene.

        Args:
            db: Sesión de base de datos
            user_id: ID del usuario
            password: Nueva contraseña

        Returns:
            True si fue exitoso
        """
        user = PersonaRepository.get_by_id(db, user_id)
        if not user:
            return False

        user.hashed_password = get_password_hash(password)
        db.commit()

        return True

    @staticmethod
    def deactivate_user(db: Session, user_id: int) -> bool:
        """
        Desactivar usuario.

        Args:
            db: Sesión de base de datos
            user_id: ID del usuario

        Returns:
            True si fue exitoso
        """
        user = PersonaRepository.get_by_id(db, user_id)
        if not user:
            return False

        user.is_active = False
        db.commit()

        return True

    @staticmethod
    def activate_user(db: Session, user_id: int) -> bool:
        """
        Activar usuario.

        Args:
            db: Sesión de base de datos
            user_id: ID del usuario

        Returns:
            True si fue exitoso
        """
        user = PersonaRepository.get_by_id(db, user_id)
        if not user:
            return False

        user.is_active = True
        db.commit()

        return True
