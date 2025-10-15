"""
Endpoints de la API para el modelo Articulo.

Este módulo define los endpoints REST para las operaciones CRUD
del modelo Articulo utilizando FastAPI.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.articulo import Articulo, ArticuloCreate, ArticuloUpdate
from app.services.articulo_service import ArticuloService

router = APIRouter(prefix="/articulos", tags=["articulos"])


@router.post("/", response_model=Articulo, status_code=status.HTTP_201_CREATED)
def create_articulo(
    articulo_data: ArticuloCreate,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo artículo.
    
    - **nombre**: Nombre del artículo
    - **descripcion**: Descripción detallada del artículo (opcional)
    - **disponible**: Estado de disponibilidad (default: true)
    
    Retorna el artículo creado con su ID asignado.
    """
    return ArticuloService.create_articulo(db, articulo_data)


@router.get("/", response_model=List[Articulo])
def get_articulos(
    skip: int = 0,
    limit: int = 100,
    disponible: Optional[bool] = Query(None, description="Filtrar por disponibilidad"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de artículos con filtros opcionales.
    
    - **skip**: Número de registros a omitir (default: 0)
    - **limit**: Máximo número de registros a retornar (default: 100)
    - **disponible**: Filtrar por disponibilidad (opcional: true/false)
    
    Retorna lista de artículos filtrados.
    """
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El límite máximo es 100 registros"
        )
    
    return ArticuloService.get_articulos(db, skip, limit, disponible)


@router.get("/disponibles", response_model=List[Articulo])
def get_articulos_disponibles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener solo artículos disponibles.
    
    - **skip**: Número de registros a omitir (default: 0)
    - **limit**: Máximo número de registros a retornar (default: 100)
    
    Retorna lista de artículos que están disponibles para reserva.
    """
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El límite máximo es 100 registros"
        )
    
    return ArticuloService.get_articulos_disponibles(db, skip, limit)


@router.get("/{articulo_id}", response_model=Articulo)
def get_articulo(
    articulo_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener un artículo específico por su ID.
    
    - **articulo_id**: ID único del artículo
    
    Retorna los datos completos del artículo.
    """
    articulo = ArticuloService.get_articulo_by_id(db, articulo_id)
    if not articulo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un artículo con ID {articulo_id}"
        )
    return articulo


@router.put("/{articulo_id}", response_model=Articulo)
def update_articulo(
    articulo_id: int,
    articulo_data: ArticuloUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar los datos de un artículo existente.
    
    - **articulo_id**: ID del artículo a actualizar
    - **nombre**: Nuevo nombre (opcional)
    - **descripcion**: Nueva descripción (opcional)
    - **disponible**: Nuevo estado de disponibilidad (opcional)
    
    Retorna los datos actualizados del artículo.
    """
    articulo = ArticuloService.update_articulo(db, articulo_id, articulo_data)
    if not articulo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un artículo con ID {articulo_id}"
        )
    return articulo


@router.patch("/{articulo_id}/toggle-disponibilidad", response_model=Articulo)
def toggle_disponibilidad(
    articulo_id: int,
    db: Session = Depends(get_db)
):
    """
    Cambiar el estado de disponibilidad de un artículo.
    
    - **articulo_id**: ID del artículo
    
    Si está disponible lo marca como no disponible y viceversa.
    Retorna el artículo con el estado actualizado.
    """
    articulo = ArticuloService.toggle_disponibilidad(db, articulo_id)
    if not articulo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un artículo con ID {articulo_id}"
        )
    return articulo


@router.delete("/{articulo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_articulo(
    articulo_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar un artículo del sistema.
    
    - **articulo_id**: ID del artículo a eliminar
    
    No retorna contenido si la eliminación es exitosa.
    Solo se puede eliminar si no tiene reservas activas.
    """
    try:
        success = ArticuloService.delete_articulo(db, articulo_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró un artículo con ID {articulo_id}"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/count/total")
def count_articulos(
    disponible: Optional[bool] = Query(None, description="Filtrar conteo por disponibilidad"),
    db: Session = Depends(get_db)
):
    """
    Obtener el número total de artículos.
    
    - **disponible**: Filtrar conteo por disponibilidad (opcional)
    
    Retorna el conteo de artículos en el sistema.
    """
    count = ArticuloService.count_articulos(db, disponible)
    return {"total": count, "disponible": disponible}