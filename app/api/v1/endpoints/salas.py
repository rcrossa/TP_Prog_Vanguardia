"""
Endpoints de la API para el modelo Sala.

Este módulo define los endpoints REST para las operaciones CRUD
del modelo Sala utilizando FastAPI.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.sala import Sala, SalaCreate, SalaUpdate
from app.services.sala_service import SalaService

router = APIRouter(prefix="/salas", tags=["salas"])


@router.post("/", response_model=Sala, status_code=status.HTTP_201_CREATED)
def create_sala(
    sala_data: SalaCreate,
    db: Session = Depends(get_db)
):
    """
    Crear una nueva sala.
    
    - **nombre**: Nombre de la sala
    - **capacidad**: Capacidad máxima de la sala (debe ser mayor a 0)
    
    Retorna la sala creada con su ID asignado.
    """
    try:
        return SalaService.create_sala(db, sala_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[Sala])
def get_salas(
    skip: int = 0,
    limit: int = 100,
    min_capacidad: Optional[int] = Query(None, description="Capacidad mínima requerida"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de salas con filtros opcionales.
    
    - **skip**: Número de registros a omitir (default: 0)
    - **limit**: Máximo número de registros a retornar (default: 100)
    - **min_capacidad**: Capacidad mínima requerida (opcional)
    
    Retorna lista de salas filtradas.
    """
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El límite máximo es 100 registros"
        )
    
    return SalaService.get_salas(db, skip, limit, min_capacidad)


@router.get("/capacidad/{min_capacidad}", response_model=List[Sala])
def get_salas_by_capacidad(
    min_capacidad: int,
    max_capacidad: Optional[int] = Query(None, description="Capacidad máxima"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener salas por rango de capacidad.
    
    - **min_capacidad**: Capacidad mínima requerida
    - **max_capacidad**: Capacidad máxima permitida (opcional)
    - **skip**: Número de registros a omitir (default: 0)
    - **limit**: Máximo número de registros a retornar (default: 100)
    
    Retorna salas que cumplan con el rango de capacidad especificado.
    """
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El límite máximo es 100 registros"
        )
    
    if min_capacidad <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La capacidad mínima debe ser mayor a 0"
        )
    
    if max_capacidad is not None and max_capacidad < min_capacidad:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La capacidad máxima debe ser mayor o igual a la mínima"
        )
    
    return SalaService.get_salas_by_capacidad(db, min_capacidad, max_capacidad, skip, limit)


@router.get("/{sala_id}", response_model=Sala)
def get_sala(
    sala_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener una sala específica por su ID.
    
    - **sala_id**: ID único de la sala
    
    Retorna los datos completos de la sala.
    """
    sala = SalaService.get_sala_by_id(db, sala_id)
    if not sala:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una sala con ID {sala_id}"
        )
    return sala


@router.put("/{sala_id}", response_model=Sala)
def update_sala(
    sala_id: int,
    sala_data: SalaUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar los datos de una sala existente.
    
    - **sala_id**: ID de la sala a actualizar
    - **nombre**: Nuevo nombre (opcional)
    - **capacidad**: Nueva capacidad (opcional, debe ser mayor a 0)
    
    Retorna los datos actualizados de la sala.
    """
    try:
        sala = SalaService.update_sala(db, sala_id, sala_data)
        if not sala:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró una sala con ID {sala_id}"
            )
        return sala
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{sala_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sala(
    sala_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar una sala del sistema.
    
    - **sala_id**: ID de la sala a eliminar
    
    No retorna contenido si la eliminación es exitosa.
    Solo se puede eliminar si no tiene reservas activas.
    """
    try:
        success = SalaService.delete_sala(db, sala_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró una sala con ID {sala_id}"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/count/total")
def count_salas(
    min_capacidad: Optional[int] = Query(None, description="Filtrar conteo por capacidad mínima"),
    db: Session = Depends(get_db)
):
    """
    Obtener el número total de salas.
    
    - **min_capacidad**: Filtrar conteo por capacidad mínima (opcional)
    
    Retorna el conteo de salas en el sistema.
    """
    count = SalaService.count_salas(db, min_capacidad)
    return {"total": count, "min_capacidad": min_capacidad}