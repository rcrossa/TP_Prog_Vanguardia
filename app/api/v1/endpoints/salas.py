"""
Endpoints de la API para el modelo Sala.

Este módulo define los endpoints REST para las operaciones CRUD
del modelo Sala utilizando FastAPI.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.sala import Sala, SalaCreate, SalaUpdate
from app.services.sala_service import SalaService

router = APIRouter(prefix="/salas", tags=["salas"])


@router.post("/", response_model=Sala, status_code=status.HTTP_201_CREATED)
def create_sala(sala_data: SalaCreate, db: Session = Depends(get_db)):
    """Crear una nueva sala."""
    try:
        return SalaService.create_sala(db, sala_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[Sala])
def get_salas(
    skip: int = 0,
    limit: int = 100,
    min_capacidad: Optional[int] = Query(
        None, description="Capacidad mínima requerida"
    ),
    db: Session = Depends(get_db),
):
    """Obtener lista de salas con filtros opcionales."""
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El límite máximo es 100 registros",
        )

    return SalaService.get_salas(db, skip, limit, min_capacidad)


@router.get("/capacidad/{min_capacidad}", response_model=List[Sala])
def get_salas_by_capacidad(
    min_capacidad: int,
    max_capacidad: Optional[int] = Query(None, description="Capacidad máxima"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Obtener salas por rango de capacidad."""
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El límite máximo es 100 registros",
        )

    if min_capacidad <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La capacidad mínima debe ser mayor a 0",
        )

    if max_capacidad is not None and max_capacidad < min_capacidad:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La capacidad máxima debe ser mayor o igual a la mínima",
        )

    return SalaService.get_salas_by_capacidad(
        db, min_capacidad, max_capacidad, skip, limit
    )


@router.get("/{sala_id}", response_model=Sala)
def get_sala(sala_id: int, db: Session = Depends(get_db)):
    """Obtener una sala específica por ID."""
    sala = SalaService.get_sala_by_id(db, sala_id)
    if not sala:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una sala con ID {sala_id}",
        )
    return sala


@router.put("/{sala_id}", response_model=Sala)
def update_sala(sala_id: int, sala_data: SalaUpdate, db: Session = Depends(get_db)):
    """Actualizar datos de una sala existente."""
    try:
        sala = SalaService.update_sala(db, sala_id, sala_data)
        if not sala:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró una sala con ID {sala_id}",
            )
        return sala
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{sala_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sala(sala_id: int, db: Session = Depends(get_db)):
    """Eliminar una sala del sistema."""
    try:
        success = SalaService.delete_sala(db, sala_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró una sala con ID {sala_id}",
            )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/count/total")
def count_salas(
    min_capacidad: Optional[int] = Query(
        None, description="Filtrar conteo por capacidad mínima"
    ),
    db: Session = Depends(get_db),
):
    """Obtener el número total de salas."""
    count = SalaService.count_salas(db, min_capacidad)
    return {"total": count, "min_capacidad": min_capacidad}
