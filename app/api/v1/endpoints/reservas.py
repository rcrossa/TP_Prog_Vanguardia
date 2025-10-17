"""
Endpoints de la API para el modelo Reserva.

Este módulo define los endpoints REST para las operaciones CRUD
del modelo Reserva utilizando FastAPI.
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.reserva import Reserva, ReservaCreate, ReservaUpdate
from app.services.reserva_service import ReservaService

router = APIRouter(prefix="/reservas", tags=["reservas"])


@router.post(
    "/",
    response_model=Reserva,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva reserva",
    description="Crear una reserva de sala o artículo con validación automática",
)
def create_reserva(reserva_data: ReservaCreate, db: Session = Depends(get_db)):
    """Crear nueva reserva de artículo o sala. Valida disponibilidad y detecta conflictos."""
    try:
        return ReservaService.create_reserva(db, reserva_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[Reserva])
def get_reservas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de reservas con paginación."""
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El límite máximo es 100 registros",
        )

    return ReservaService.get_reservas(db, skip, limit)


@router.get("/{reserva_id}", response_model=Reserva)
def get_reserva(reserva_id: int, db: Session = Depends(get_db)):
    """Obtener una reserva específica por ID."""
    reserva = ReservaService.get_reserva_by_id(db, reserva_id)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una reserva con ID {reserva_id}",
        )
    return reserva


@router.get("/persona/{persona_id}", response_model=List[Reserva])
def get_reservas_by_persona(
    persona_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener reservas de una persona específica."""
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El límite máximo es 100 registros",
        )

    return ReservaService.get_reservas_by_persona(db, persona_id, skip, limit)


@router.get("/sala/{sala_id}", response_model=List[Reserva])
def get_reservas_by_sala(
    sala_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener reservas de una sala específica."""
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El límite máximo es 100 registros",
        )

    return ReservaService.get_reservas_by_sala(db, sala_id, skip, limit)


@router.get("/articulo/{articulo_id}", response_model=List[Reserva])
def get_reservas_by_articulo(
    articulo_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener reservas de un artículo específico."""
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El límite máximo es 100 registros",
        )

    return ReservaService.get_reservas_by_articulo(db, articulo_id, skip, limit)


@router.get("/fechas/rango", response_model=List[Reserva])
def get_reservas_by_fecha_range(
    fecha_inicio: datetime = Query(..., description="Fecha y hora de inicio del rango"),
    fecha_fin: Optional[datetime] = Query(
        None, description="Fecha y hora de fin del rango"
    ),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Obtener reservas en un rango de fechas."""
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El límite máximo es 100 registros",
        )

    if fecha_fin and fecha_fin <= fecha_inicio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de fin debe ser posterior a la fecha de inicio",
        )

    return ReservaService.get_reservas_by_fecha_range(
        db, fecha_inicio, fecha_fin, skip, limit
    )


@router.get("/sala/{sala_id}/disponibilidad")
def check_sala_availability(
    sala_id: int,
    fecha_inicio: datetime = Query(..., description="Fecha y hora de inicio"),
    fecha_fin: datetime = Query(..., description="Fecha y hora de fin"),
    db: Session = Depends(get_db),
):
    """Verificar disponibilidad de sala en un horario específico."""
    if fecha_fin <= fecha_inicio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de fin debe ser posterior a la fecha de inicio",
        )

    disponible = ReservaService.check_sala_availability(
        db, sala_id, fecha_inicio, fecha_fin
    )

    return {
        "sala_id": sala_id,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "disponible": disponible,
    }


@router.put("/{reserva_id}", response_model=Reserva)
def update_reserva(
    reserva_id: int, reserva_data: ReservaUpdate, db: Session = Depends(get_db)
):
    """Actualizar una reserva existente."""
    try:
        reserva = ReservaService.update_reserva(db, reserva_id, reserva_data)
        if not reserva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró una reserva con ID {reserva_id}",
            )
        return reserva
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{reserva_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reserva(reserva_id: int, db: Session = Depends(get_db)):
    """Eliminar una reserva del sistema."""
    success = ReservaService.delete_reserva(db, reserva_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una reserva con ID {reserva_id}",
        )


@router.get("/count/total")
def count_reservas(db: Session = Depends(get_db)):
    """Obtener el número total de reservas."""
    count = ReservaService.count_reservas(db)
    return {"total": count}


@router.get("/{reserva_id}/articulos")
def get_articulos_reserva(reserva_id: int, db: Session = Depends(get_db)):
    """Obtener artículos asignados a una reserva de sala."""
    result = db.execute(
        text(
            """
        SELECT a.id, a.nombre, a.descripcion, a.categoria, ra.cantidad
        FROM reserva_articulos ra
        JOIN articulos a ON ra.articulo_id = a.id
        WHERE ra.reserva_id = :reserva_id
        """
        ),
        {"reserva_id": reserva_id},
    )
    articulos = [
        {
            "id": row[0],
            "nombre": row[1],
            "descripcion": row[2],
            "categoria": row[3],
            "cantidad": row[4],
        }
        for row in result
    ]
    return articulos


@router.post("/{reserva_id}/articulos/{articulo_id}")
def add_articulo_to_reserva(
    reserva_id: int,
    articulo_id: int,
    cantidad: int = Query(1, ge=1),
    modo: str = Query(
        "sumar",
        description="'sumar' para agregar, 'reemplazar' para establecer cantidad exacta",
    ),
    db: Session = Depends(get_db),
):
    """Agregar o actualizar artículo en una reserva de sala."""
    # Verificar que la reserva existe
    from app.repositories.reserva_repository import ReservaRepository

    reserva = ReservaRepository.get_by_id(db, reserva_id)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una reserva con ID {reserva_id}",
        )

    if not reserva.id_sala:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden asignar artículos a reservas de salas",
        )

    # Verificar que el artículo existe y obtener su cantidad total
    from app.repositories.articulo_repository import ArticuloRepository

    articulo = ArticuloRepository.get_by_id(db, articulo_id)
    if not articulo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un artículo con ID {articulo_id}",
        )

    if not articulo.disponible:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El artículo '{articulo.nombre}' no está disponible para reservas",
        )

    # Primero verificar si ya existe la asignación
    existing = db.execute(
        text(
            """
        SELECT cantidad FROM reserva_articulos
        WHERE reserva_id = :reserva_id AND articulo_id = :articulo_id
        """
        ),
        {"reserva_id": reserva_id, "articulo_id": articulo_id},
    ).fetchone()

    cantidad_ya_asignada = existing[0] if existing else 0

    # Calcular cantidad reservada en el mismo período de tiempo (EXCLUYENDO la reserva actual)
    # Incluye reservas directas del artículo Y artículos en reservas de sala
    result = db.execute(
        text(
            """
        SELECT COALESCE(SUM(cantidad_usada), 0) as total_reservado
        FROM (
            -- Reservas directas del artículo
            SELECT 1 as cantidad_usada
            FROM reservas r
            WHERE r.id_articulo = :articulo_id
            AND r.id != :reserva_id
            AND r.fecha_hora_fin >= :fecha_inicio
            AND r.fecha_hora_inicio <= :fecha_fin

            UNION ALL

            -- Artículos en reservas de sala (EXCLUYENDO esta reserva)
            SELECT ra.cantidad as cantidad_usada
            FROM reserva_articulos ra
            JOIN reservas r ON ra.reserva_id = r.id
            WHERE ra.articulo_id = :articulo_id
            AND ra.reserva_id != :reserva_id
            AND r.fecha_hora_fin >= :fecha_inicio
            AND r.fecha_hora_inicio <= :fecha_fin
        ) as reservas_activas
        """
        ),
        {
            "articulo_id": articulo_id,
            "reserva_id": reserva_id,
            "fecha_inicio": reserva.fecha_hora_inicio,
            "fecha_fin": reserva.fecha_hora_fin,
        },
    )

    total_reservado_otras = result.scalar() or 0

    # Calcular disponibilidad considerando lo que ya tiene asignado esta reserva
    # Total disponible = Stock total - Reservado en otras - Lo que YA tiene esta reserva
    cantidad_disponible_para_agregar = (
        articulo.cantidad - total_reservado_otras - cantidad_ya_asignada
    )

    if existing:
        # Ya existe - decidir si SUMAR o REEMPLAZAR
        if modo == "reemplazar":
            nueva_cantidad = cantidad
        else:  # modo == "sumar" (default)
            nueva_cantidad = cantidad_ya_asignada + cantidad

        # Validar que no exceda el stock total
        if nueva_cantidad > articulo.cantidad - total_reservado_otras:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No hay suficiente cantidad disponible. Ya asignado en esta reserva: {cantidad_ya_asignada}, {'Quieres establecer' if modo == 'reemplazar' else 'Quieres agregar'}: {cantidad}, Total necesario: {nueva_cantidad}, Disponible: {articulo.cantidad - total_reservado_otras} (Stock total: {articulo.cantidad}, Reservado en otras: {total_reservado_otras})",
            )

        db.execute(
            text(
                """
            UPDATE reserva_articulos
            SET cantidad = :nueva_cantidad
            WHERE reserva_id = :reserva_id AND articulo_id = :articulo_id
            """
            ),
            {
                "reserva_id": reserva_id,
                "articulo_id": articulo_id,
                "nueva_cantidad": nueva_cantidad,
            },
        )
    else:
        # No existe - INSERTAR nuevo registro
        # Validar que no exceda el stock disponible
        if cantidad > cantidad_disponible_para_agregar:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No hay suficiente cantidad disponible. Solicitado: {cantidad}, Disponible: {cantidad_disponible_para_agregar} (Stock total: {articulo.cantidad}, Reservado en otras: {total_reservado_otras})",
            )

        db.execute(
            text(
                """
            INSERT INTO reserva_articulos (reserva_id, articulo_id, cantidad)
            VALUES (:reserva_id, :articulo_id, :cantidad)
            """
            ),
            {
                "reserva_id": reserva_id,
                "articulo_id": articulo_id,
                "cantidad": cantidad,
            },
        )

    db.commit()

    return {"message": "Artículo agregado a la reserva exitosamente"}


@router.delete("/{reserva_id}/articulos/{articulo_id}")
def remove_articulo_from_reserva(
    reserva_id: int, articulo_id: int, db: Session = Depends(get_db)
):
    """Eliminar un artículo de una reserva de sala."""
    result = db.execute(
        text(
            """
        DELETE FROM reserva_articulos
        WHERE reserva_id = :reserva_id AND articulo_id = :articulo_id
        """
        ),
        {"reserva_id": reserva_id, "articulo_id": articulo_id},
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró el artículo en la reserva",
        )

    return {"message": "Artículo eliminado de la reserva exitosamente"}
