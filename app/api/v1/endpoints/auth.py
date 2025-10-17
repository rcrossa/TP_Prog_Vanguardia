"""
Endpoints de autenticación para el Sistema de Reservas.

Este módulo define los endpoints REST para login, registro,
cambio de contraseña y gestión de usuarios.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, get_current_admin_user
from app.core.database import get_db
from app.models.persona import Persona
from app.repositories.persona_repository import PersonaRepository
from app.schemas.auth import (
    LoginResponse,
    UserChangePassword,
    UserLogin,
    UserProfile,
    UserRegister,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["🔐 Autenticación"])


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="🔑 Iniciar Sesión",
    description="Autenticar usuario con email y contraseña, retorna token JWT",
    responses={
        200: {
            "description": "Login exitoso",
            "content": {
                "application/json": {
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
            },
        },
        401: {
            "description": "Credenciales incorrectas",
            "content": {
                "application/json": {
                    "example": {"detail": "Email o contraseña incorrectos"}
                }
            },
        },
    },
)
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    ## 🔑 Iniciar Sesión

    Autentica un usuario con su email y contraseña, y retorna un token JWT
    para acceder a los endpoints protegidos.

    ### 📝 Campos Requeridos
    - **email**: Email registrado en el sistema
    - **password**: Contraseña del usuario

    ### 🎫 Token JWT
    El token retornado debe incluirse en el header `Authorization: Bearer <token>`
    para acceder a endpoints protegidos.

    ### ⏰ Expiración
    El token tiene una duración de 30 minutos. Después de este tiempo será
    necesario hacer login nuevamente.

    ### 💡 Ejemplo de Uso
    ```bash
    curl -X POST "http://localhost:8000/auth/login" \\
         -H "Content-Type: application/json" \\
         -d '{"email": "juan@ejemplo.com", "password": "micontraseña"}'
    ```
    """
    return AuthService.login_user(db, login_data)


@router.post(
    "/register",
    response_model=UserProfile,
    status_code=status.HTTP_201_CREATED,
    summary="📝 Registrar Usuario",
    description="Crear nueva cuenta de usuario en el sistema",
    responses={
        201: {
            "description": "Usuario registrado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "nombre": "Juan Pérez",
                        "email": "juan@ejemplo.com",
                        "is_active": True,
                        "is_admin": False,
                        "has_password": True,
                    }
                }
            },
        },
        400: {
            "description": "Error de validación",
            "content": {
                "application/json": {
                    "examples": {
                        "passwords_not_match": {
                            "summary": "Contraseñas no coinciden",
                            "value": {"detail": "Las contraseñas no coinciden"},
                        },
                        "email_exists": {
                            "summary": "Email ya existe",
                            "value": {
                                "detail": "Ya existe un usuario con el email juan@ejemplo.com"
                            },
                        },
                    }
                }
            },
        },
    },
)
async def register(register_data: UserRegister, db: Session = Depends(get_db)):
    """
    ## 📝 Registrar Nueva Cuenta

    Crea una nueva cuenta de usuario en el sistema con email único y contraseña segura.

    ### 📋 Campos Requeridos
    - **nombre**: Nombre completo (mínimo 2 caracteres)
    - **email**: Email único y válido
    - **password**: Contraseña segura (mínimo 6 caracteres)
    - **confirm_password**: Confirmación de contraseña (debe coincidir)

    ### ✅ Validaciones Automáticas
    - Email debe ser único en el sistema
    - Contraseñas deben coincidir
    - Email debe tener formato válido
    - Nombre debe tener al menos 2 caracteres

    ### 🔐 Seguridad
    Las contraseñas se almacenan usando hash bcrypt seguro.
    Nunca se almacenan contraseñas en texto plano.

    ### 💡 Ejemplo de Uso
    ```json
    {
        "nombre": "María González",
        "email": "maria@universidad.edu",
        "password": "micontraseña123",
        "confirm_password": "micontraseña123"
    }
    ```
    """
    user = AuthService.register_user(db, register_data)

    return UserProfile(
        id=user.id,
        nombre=user.nombre,
        email=user.email,
        is_active=user.is_active,
        is_admin=user.is_admin,
        created_at=user.created_at,
        last_login=user.last_login,
        has_password=user.has_password(),
    )


@router.get(
    "/me",
    response_model=UserProfile,
    summary="👤 Perfil Usuario",
    description="Obtener información del usuario autenticado actual",
)
async def get_user_profile(current_user: Persona = Depends(get_current_active_user)):
    """
    ## 👤 Obtener Perfil de Usuario

    Retorna la información completa del usuario autenticado actual.

    ### 🔐 Autenticación Requerida
    Este endpoint requiere un token JWT válido en el header:
    ```
    Authorization: Bearer <tu_token_jwt>
    ```

    ### 📊 Información Incluida
    - Datos personales (nombre, email)
    - Estado de la cuenta (activo, administrador)
    - Fechas importantes (creación, último login)
    - Estado de seguridad (tiene contraseña)

    ### 💡 Ejemplo de Uso
    ```bash
    curl -X GET "http://localhost:8000/auth/me" \\
         -H "Authorization: Bearer tu_token_jwt"
    ```
    """
    return UserProfile(
        id=current_user.id,
        nombre=current_user.nombre,
        email=current_user.email,
        is_active=current_user.is_active,
        is_admin=current_user.is_admin,
        created_at=current_user.created_at,
        last_login=current_user.last_login,
        has_password=current_user.has_password(),
    )


@router.post(
    "/change-password",
    summary="🔒 Cambiar Contraseña",
    description="Cambiar contraseña del usuario autenticado",
)
async def change_password(
    password_data: UserChangePassword,
    current_user: Persona = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    ## 🔒 Cambiar Contraseña

    Permite al usuario autenticado cambiar su contraseña actual por una nueva.

    ### 🔐 Autenticación Requerida
    Requiere token JWT válido del usuario cuya contraseña se va a cambiar.

    ### 📝 Campos Requeridos
    - **current_password**: Contraseña actual (para verificación)
    - **new_password**: Nueva contraseña (mínimo 6 caracteres)
    - **confirm_new_password**: Confirmación de nueva contraseña

    ### ✅ Validaciones
    - Contraseña actual debe ser correcta
    - Nueva contraseña debe tener mínimo 6 caracteres
    - Confirmación debe coincidir con nueva contraseña

    ### 🛡️ Seguridad
    - Se verifica la contraseña actual antes de cambiar
    - Nueva contraseña se hashea de forma segura
    - Se invalidan todos los tokens existentes (implícito)
    """
    AuthService.change_password(db, current_user.id, password_data)
    return {"message": "Contraseña cambiada exitosamente"}


@router.post(
    "/logout",
    summary="🚪 Cerrar Sesión",
    description="Cerrar sesión del usuario (información para el cliente)",
)
async def logout(current_user: Persona = Depends(get_current_active_user)):
    """
    ## 🚪 Cerrar Sesión

    Cierra la sesión del usuario actual. Como usamos JWT stateless,
    el cliente debe descartar el token localmente.

    ### 💡 Nota Importante
    Los tokens JWT son stateless, por lo que técnicamente siguen siendo
    válidos hasta su expiración natural. El cliente debe:

    1. Eliminar el token del almacenamiento local
    2. Redirigir al usuario a la página de login
    3. No incluir el token en futuras requests

    ### 🔐 Token Cleanup
    Para invalidación inmediata de tokens, se requeriría implementar
    una blacklist de tokens en el servidor (funcionalidad avanzada).
    """
    return {
        "message": "Sesión cerrada exitosamente",
        "user": current_user.nombre,
        "instructions": "Elimina el token del cliente y redirige al login",
    }


# Endpoints administrativos
@router.get(
    "/users",
    response_model=list[UserProfile],
    summary="👥 Listar Usuarios (Admin)",
    description="Obtener lista de todos los usuarios - Solo administradores",
)
async def list_users(
    db: Session = Depends(get_db), admin_user: Persona = Depends(get_current_admin_user)
):
    """
    ## 👥 Listar Todos los Usuarios

    Obtiene una lista de todos los usuarios registrados en el sistema.

    ### 🛡️ Permisos Requeridos
    Solo usuarios con permisos de administrador pueden acceder a este endpoint.

    ### 📊 Información Incluida
    Para cada usuario se incluye:
    - Información personal básica
    - Estado de la cuenta
    - Fechas de actividad
    - Configuración de seguridad
    """
    # Implementar paginación en el futuro
    users = PersonaRepository.get_all(db, limit=100)

    return [
        UserProfile(
            id=user.id,
            nombre=user.nombre,
            email=user.email,
            is_active=user.is_active,
            is_admin=user.is_admin,
            created_at=user.created_at,
            last_login=user.last_login,
            has_password=user.has_password(),
        )
        for user in users
    ]


@router.patch(
    "/users/{user_id}/toggle-active",
    summary="🔄 Activar/Desactivar Usuario (Admin)",
    description="Cambiar estado activo de un usuario - Solo administradores",
)
async def toggle_user_active(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: Persona = Depends(get_current_admin_user),
):
    """
    ## 🔄 Activar/Desactivar Usuario

    Permite a un administrador cambiar el estado activo de cualquier usuario.

    ### 🛡️ Permisos Requeridos
    Solo usuarios administradores pueden usar este endpoint.

    ### ⚠️ Consideraciones
    - Usuarios desactivados no pueden hacer login
    - Los tokens existentes seguirán siendo válidos hasta expirar
    - El usuario no podrá generar nuevos tokens
    """
    user = PersonaRepository.get_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    # No permitir desactivar el propio usuario admin
    if user.id == admin_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes desactivar tu propia cuenta",
        )

    if user.is_active:
        AuthService.deactivate_user(db, user_id)
        action = "desactivado"
    else:
        AuthService.activate_user(db, user_id)
        action = "activado"

    return {
        "message": f"Usuario {action} exitosamente",
        "user_id": user_id,
        "user_name": user.nombre,
        "new_status": not user.is_active,
    }
