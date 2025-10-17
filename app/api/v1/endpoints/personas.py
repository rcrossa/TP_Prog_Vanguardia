"""
Endpoints de la API para el modelo Persona.

Este módulo define los endpoints REST para las operaciones CRUD
del modelo Persona utilizando FastAPI.
"""

from typing import List
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.persona import Persona, PersonaCreate, PersonaUpdate, PersonaLogin, PersonaLoginResponse
from app.services.persona_service import PersonaService, ACCESS_TOKEN_EXPIRE_MINUTES
from app.auth.dependencies import get_current_admin_user, get_current_user
from app.auth.jwt_handler import create_access_token
from app.models.persona import Persona as PersonaModel

router = APIRouter(prefix="/personas", tags=["personas"])


@router.post(
    "/", 
    response_model=Persona, 
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva persona",
    description="Registra una nueva persona en el sistema (solo administradores)"
)
def create_persona(
    persona_data: PersonaCreate,
    db: Session = Depends(get_db),
    current_user: PersonaModel = Depends(get_current_admin_user)
):
    """Crear nueva persona en el sistema (solo administradores)."""
    try:
        return PersonaService.create_persona(db, persona_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=PersonaLoginResponse)
def login_user(login_data: PersonaLogin, db: Session = Depends(get_db)):
    """Autenticar usuario y obtener token de acceso."""
    user = PersonaService.authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=Persona)
def get_current_user_info(current_user: PersonaModel = Depends(get_current_user)):
    """Obtener información del usuario autenticado."""
    return current_user


@router.get("/", response_model=List[Persona])
def get_personas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: PersonaModel = Depends(get_current_admin_user)
):
    """Obtener lista de personas con paginación (solo administradores)."""
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El límite máximo es 100 registros"
        )
    
    return PersonaService.get_personas(db, skip, limit)


@router.get("/{persona_id}", response_model=Persona)
def get_persona(
    persona_id: int,
    db: Session = Depends(get_db),
    current_user: PersonaModel = Depends(get_current_admin_user)
):
    """Obtener una persona específica por ID."""
    persona = PersonaService.get_persona_by_id(db, persona_id)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una persona con ID {persona_id}"
        )
    return persona


@router.get("/email/{email}", response_model=Persona)
def get_persona_by_email(
    email: str,
    db: Session = Depends(get_db),
    current_user: PersonaModel = Depends(get_current_admin_user)
):
    """Obtener una persona por su email.
    
    - **email**: Dirección de email de la persona
    
    Retorna los datos de la persona si existe.
    """
    persona = PersonaService.get_persona_by_email(db, email)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una persona con email {email}"
        )
    return persona


@router.put("/{persona_id}", response_model=Persona)
def update_persona(
    persona_id: int,
    persona_data: PersonaUpdate,
    db: Session = Depends(get_db),
    current_user: PersonaModel = Depends(get_current_admin_user)
):
    """Actualizar datos de una persona existente."""
    try:
        persona = PersonaService.update_persona(db, persona_id, persona_data)
        if not persona:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró una persona con ID {persona_id}"
            )
        return persona
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_persona(
    persona_id: int,
    db: Session = Depends(get_db),
    current_user: PersonaModel = Depends(get_current_admin_user)
):
    """Eliminar una persona del sistema."""
    try:
        success = PersonaService.delete_persona(db, persona_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró una persona con ID {persona_id}"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/count/total")
def count_personas(
    db: Session = Depends(get_db),
    current_user: PersonaModel = Depends(get_current_admin_user)
):
    """Obtener el número total de personas registradas."""
    count = PersonaService.count_personas(db)
    return {"total": count}


@router.post("/web-login")
def web_login_user(login_data: PersonaLogin, db: Session = Depends(get_db)):
    """Autenticar usuario para navegación web y configurar cookies."""
    from fastapi.responses import JSONResponse
    
    user = PersonaService.authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}, 
        expires_delta=access_token_expires
    )
    
    # Crear respuesta JSON
    response_data = {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "nombre": user.nombre,
            "email": user.email,
            "is_admin": user.is_admin,
            "is_active": user.is_active
        }
    }
    
    # Crear respuesta con cookies
    response = JSONResponse(content=response_data)
    
    # Configurar cookie con el token
    response.set_cookie(
        key="token",
        value=access_token,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # En segundos
        path="/",        # Disponible en todas las rutas
        httponly=False,  # Permitir acceso desde JavaScript
        secure=False,    # False para desarrollo en localhost
        samesite="lax"   # Política de cookies
    )
    
    return response