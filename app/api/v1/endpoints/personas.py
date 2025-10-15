"""
Endpoints de la API para el modelo Persona.

Este módulo define los endpoints REST para las operaciones CRUD
del modelo Persona utilizando FastAPI.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.persona import Persona, PersonaCreate, PersonaUpdate
from app.services.persona_service import PersonaService

router = APIRouter(prefix="/personas", tags=["personas"])


@router.post(
    "/", 
    response_model=Persona, 
    status_code=status.HTTP_201_CREATED,
    summary="➕ Crear nueva persona",
    description="Registra una nueva persona en el sistema con validación de email único",
    response_description="Persona creada exitosamente con ID asignado",
    responses={
        201: {
            "description": "Persona creada exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "nombre": "Juan Pérez",
                        "email": "juan.perez@email.com"
                    }
                }
            }
        },
        400: {
            "description": "Error de validación - Email ya existe o datos inválidos",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Ya existe una persona con el email juan.perez@email.com"
                    }
                }
            }
        }
    }
)
def create_persona(
    persona_data: PersonaCreate,
    db: Session = Depends(get_db)
):
    """
    ## 👤 Crear una nueva persona
    
    Registra una nueva persona en el sistema con las siguientes validaciones:
    
    ### 📝 Campos Requeridos
    - **nombre**: Nombre completo de la persona (mínimo 2 caracteres)
    - **email**: Dirección de email válida y única en el sistema
    
    ### ✅ Validaciones Automáticas
    - Email debe tener formato válido
    - Email debe ser único (no puede repetirse)
    - Nombre no puede estar vacío
    
    ### 📤 Respuesta
    Retorna la persona creada con su ID único asignado automáticamente.
    
    ### 💡 Ejemplo de Uso
    ```json
    {
        "nombre": "María González",
        "email": "maria.gonzalez@universidad.edu"
    }
    ```
    """
    try:
        return PersonaService.create_persona(db, persona_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[Persona])
def get_personas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener lista de personas con paginación.
    
    - **skip**: Número de registros a omitir (default: 0)
    - **limit**: Máximo número de registros a retornar (default: 100)
    
    Retorna lista de personas ordenadas por ID.
    """
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El límite máximo es 100 registros"
        )
    
    return PersonaService.get_personas(db, skip, limit)


@router.get("/{persona_id}", response_model=Persona)
def get_persona(
    persona_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener una persona específica por su ID.
    
    - **persona_id**: ID único de la persona
    
    Retorna los datos completos de la persona.
    """
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
    db: Session = Depends(get_db)
):
    """
    Obtener una persona por su dirección de email.
    
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
    db: Session = Depends(get_db)
):
    """
    Actualizar los datos de una persona existente.
    
    - **persona_id**: ID de la persona a actualizar
    - **nombre**: Nuevo nombre (opcional)
    - **email**: Nuevo email (opcional, debe ser único)
    
    Retorna los datos actualizados de la persona.
    """
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
    db: Session = Depends(get_db)
):
    """
    Eliminar una persona del sistema.
    
    - **persona_id**: ID de la persona a eliminar
    
    No retorna contenido si la eliminación es exitosa.
    Solo se puede eliminar si no tiene reservas activas.
    """
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
def count_personas(db: Session = Depends(get_db)):
    """
    Obtener el número total de personas registradas.
    
    Retorna el conteo total de personas en el sistema.
    """
    count = PersonaService.count_personas(db)
    return {"total": count}