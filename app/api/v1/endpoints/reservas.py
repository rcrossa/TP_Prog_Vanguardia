"""
Endpoints de la API para el modelo Reserva.

Este módulo define los endpoints REST para las operaciones CRUD
del modelo Reserva utilizando FastAPI.
"""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.reserva import Reserva, ReservaCreate, ReservaUpdate
from app.services.reserva_service import ReservaService

router = APIRouter(prefix="/reservas", tags=["reservas"])


@router.post(
    "/", 
    response_model=Reserva, 
    status_code=status.HTTP_201_CREATED,
    summary="🎯 Crear nueva reserva",
    description="Sistema inteligente de reservas con detección automática de conflictos",
    response_description="Reserva creada exitosamente con validaciones completadas",
    responses={
        201: {
            "description": "Reserva creada exitosamente",
            "content": {
                "application/json": {
                    "examples": {
                        "reserva_articulo": {
                            "summary": "Reserva de Artículo",
                            "description": "Ejemplo de reserva de un artículo (ej: laptop, proyector)",
                            "value": {
                                "id": 1,
                                "id_persona": 1,
                                "fecha_hora_inicio": "2025-10-16T09:00:00",
                                "fecha_hora_fin": "2025-10-16T17:00:00",
                                "id_articulo": 1,
                                "id_sala": None
                            }
                        },
                        "reserva_sala": {
                            "summary": "Reserva de Sala", 
                            "description": "Ejemplo de reserva de una sala de reuniones",
                            "value": {
                                "id": 2,
                                "id_persona": 2,
                                "fecha_hora_inicio": "2025-10-17T14:00:00",
                                "fecha_hora_fin": "2025-10-17T16:00:00",
                                "id_articulo": None,
                                "id_sala": 1
                            }
                        }
                    }
                }
            }
        },
        400: {
            "description": "Error de validación o conflicto detectado",
            "content": {
                "application/json": {
                    "examples": {
                        "conflicto_horario": {
                            "summary": "Conflicto de Horario",
                            "value": {
                                "detail": "Ya existe una reserva en la sala para el horario especificado"
                            }
                        },
                        "articulo_no_disponible": {
                            "summary": "Artículo No Disponible",
                            "value": {
                                "detail": "El artículo con ID 1 no existe o no está disponible"
                            }
                        },
                        "fecha_invalida": {
                            "summary": "Fechas Inválidas",
                            "value": {
                                "detail": "La fecha de fin debe ser posterior a la fecha de inicio"
                            }
                        }
                    }
                }
            }
        }
    }
)
def create_reserva(
    reserva_data: ReservaCreate,
    db: Session = Depends(get_db)
):
    """
    ## 🎯 Crear Nueva Reserva Inteligente
    
    Sistema avanzado de reservas que valida automáticamente disponibilidad y detecta conflictos.
    
    ### 📋 Tipos de Reserva
    
    **🔹 Reserva de Artículo** (Equipos, Libros, etc.)
    - Especifica `id_articulo` y deja `id_sala` como `null`
    - El sistema verifica que el artículo esté disponible
    - Ideal para: laptops, proyectores, libros, equipos
    
    **🔹 Reserva de Sala** (Espacios Físicos)
    - Especifica `id_sala` y deja `id_articulo` como `null`
    - El sistema detecta automáticamente conflictos de horario
    - Ideal para: salas de reuniones, aulas, auditorios
    
    ### ✅ Validaciones Automáticas
    
    - 👤 **Persona existe** - Verifica que el ID de persona sea válido
    - 📅 **Fechas lógicas** - Fin posterior al inicio, no en el pasado
    - 📦 **Disponibilidad** - Artículo debe estar disponible (si aplica)
    - ⚡ **Conflictos** - Detección automática de solapamientos (salas)
    - 🚫 **Exclusividad** - Solo artículo O sala, no ambos
    
    ### 🚨 Reglas de Negocio
    
    1. **Una reserva = UN recurso**: Artículo XOR Sala
    2. **No pasado**: No se permiten reservas retroactivas
    3. **Duraciones lógicas**: Fin > Inicio siempre
    4. **Sin solapamientos**: Salas no pueden tener conflictos
    5. **Disponibilidad**: Artículos deben estar disponibles
    
    ### 💡 Casos de Uso Típicos
    
    ```json
    // Reservar laptop para trabajo remoto
    {
        "id_persona": 1,
        "fecha_hora_inicio": "2025-10-16T09:00:00",
        "fecha_hora_fin": "2025-10-16T17:00:00",
        "id_articulo": 5,
        "id_sala": null
    }
    
    // Reservar sala para reunión
    {
        "id_persona": 2,
        "fecha_hora_inicio": "2025-10-17T14:00:00", 
        "fecha_hora_fin": "2025-10-17T16:00:00",
        "id_articulo": null,
        "id_sala": 3
    }
    ```
    """
    try:
        return ReservaService.create_reserva(db, reserva_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[Reserva])
def get_reservas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener lista de reservas con paginación.
    
    - **skip**: Número de registros a omitir (default: 0)
    - **limit**: Máximo número de registros a retornar (default: 100)
    
    Retorna lista de reservas con relaciones cargadas (persona, sala, artículo).
    """
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El límite máximo es 100 registros"
        )
    
    return ReservaService.get_reservas(db, skip, limit)


@router.get("/{reserva_id}", response_model=Reserva)
def get_reserva(
    reserva_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener una reserva específica por su ID.
    
    - **reserva_id**: ID único de la reserva
    
    Retorna los datos completos de la reserva con relaciones.
    """
    reserva = ReservaService.get_reserva_by_id(db, reserva_id)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una reserva con ID {reserva_id}"
        )
    return reserva


@router.get("/persona/{persona_id}", response_model=List[Reserva])
def get_reservas_by_persona(
    persona_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener todas las reservas de una persona específica.
    
    - **persona_id**: ID de la persona
    - **skip**: Número de registros a omitir (default: 0)
    - **limit**: Máximo número de registros a retornar (default: 100)
    
    Retorna lista de reservas de la persona especificada.
    """
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El límite máximo es 100 registros"
        )
    
    return ReservaService.get_reservas_by_persona(db, persona_id, skip, limit)


@router.get("/sala/{sala_id}", response_model=List[Reserva])
def get_reservas_by_sala(
    sala_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener todas las reservas de una sala específica.
    
    - **sala_id**: ID de la sala
    - **skip**: Número de registros a omitir (default: 0)
    - **limit**: Máximo número de registros a retornar (default: 100)
    
    Retorna lista de reservas de la sala especificada.
    """
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El límite máximo es 100 registros"
        )
    
    return ReservaService.get_reservas_by_sala(db, sala_id, skip, limit)


@router.get("/articulo/{articulo_id}", response_model=List[Reserva])
def get_reservas_by_articulo(
    articulo_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener todas las reservas de un artículo específico.
    
    - **articulo_id**: ID del artículo
    - **skip**: Número de registros a omitir (default: 0)
    - **limit**: Máximo número de registros a retornar (default: 100)
    
    Retorna lista de reservas del artículo especificado.
    """
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El límite máximo es 100 registros"
        )
    
    return ReservaService.get_reservas_by_articulo(db, articulo_id, skip, limit)


@router.get("/fechas/rango", response_model=List[Reserva])
def get_reservas_by_fecha_range(
    fecha_inicio: datetime = Query(..., description="Fecha y hora de inicio del rango"),
    fecha_fin: Optional[datetime] = Query(None, description="Fecha y hora de fin del rango"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener reservas en un rango de fechas.
    
    - **fecha_inicio**: Fecha y hora de inicio del rango (requerido)
    - **fecha_fin**: Fecha y hora de fin del rango (opcional)
    - **skip**: Número de registros a omitir (default: 0)
    - **limit**: Máximo número de registros a retornar (default: 100)
    
    Retorna reservas que se solapen con el rango de fechas especificado.
    """
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El límite máximo es 100 registros"
        )
    
    if fecha_fin and fecha_fin <= fecha_inicio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de fin debe ser posterior a la fecha de inicio"
        )
    
    return ReservaService.get_reservas_by_fecha_range(db, fecha_inicio, fecha_fin, skip, limit)


@router.get("/sala/{sala_id}/disponibilidad")
def check_sala_availability(
    sala_id: int,
    fecha_inicio: datetime = Query(..., description="Fecha y hora de inicio"),
    fecha_fin: datetime = Query(..., description="Fecha y hora de fin"),
    db: Session = Depends(get_db)
):
    """
    Verificar disponibilidad de una sala en un horario específico.
    
    - **sala_id**: ID de la sala a verificar
    - **fecha_inicio**: Fecha y hora de inicio deseada
    - **fecha_fin**: Fecha y hora de fin deseada
    
    Retorna si la sala está disponible en el horario solicitado.
    """
    if fecha_fin <= fecha_inicio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de fin debe ser posterior a la fecha de inicio"
        )
    
    disponible = ReservaService.check_sala_availability(db, sala_id, fecha_inicio, fecha_fin)
    
    return {
        "sala_id": sala_id,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "disponible": disponible
    }


@router.put("/{reserva_id}", response_model=Reserva)
def update_reserva(
    reserva_id: int,
    reserva_data: ReservaUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar una reserva existente.
    
    - **reserva_id**: ID de la reserva a actualizar
    - **id_persona**: Nuevo ID de persona (opcional)
    - **fecha_hora_inicio**: Nueva fecha/hora de inicio (opcional)
    - **fecha_hora_fin**: Nueva fecha/hora de fin (opcional)
    - **id_articulo**: Nuevo ID de artículo (opcional)
    - **id_sala**: Nuevo ID de sala (opcional)
    
    Retorna los datos actualizados de la reserva.
    """
    try:
        reserva = ReservaService.update_reserva(db, reserva_id, reserva_data)
        if not reserva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró una reserva con ID {reserva_id}"
            )
        return reserva
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{reserva_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reserva(
    reserva_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar una reserva del sistema.
    
    - **reserva_id**: ID de la reserva a eliminar
    
    No retorna contenido si la eliminación es exitosa.
    """
    success = ReservaService.delete_reserva(db, reserva_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una reserva con ID {reserva_id}"
        )


@router.get("/count/total")
def count_reservas(db: Session = Depends(get_db)):
    """
    Obtener el número total de reservas.
    
    Retorna el conteo total de reservas en el sistema.
    """
    count = ReservaService.count_reservas(db)
    return {"total": count}