""" Reservas API endpoints."""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.articulo_repository import ArticuloRepository
from app.repositories.reserva_repository import ReservaRepository
from app.schemas.reserva import Reserva, ReservaCreate, ReservaUpdate
from app.services.reserva_service import ReservaService
from app.auth.dependencies import (
    get_current_user,
)
from app.models.persona import Persona as PersonaModel
def _verificar_reserva_existente(db, reserva_id):
    reserva = ReservaRepository.get_by_id(db, reserva_id)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una reserva con ID {reserva_id}",
        )
    return reserva

def _verificar_permiso_modificar_reserva(reserva, current_user):
    if not current_user.is_admin and reserva.id_persona != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para modificar los artículos de esta reserva",
        )

def _verificar_reserva_es_sala(reserva):
    if not reserva.id_sala:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden asignar artículos a reservas de salas",
        )

def _verificar_articulo_existente(db, articulo_id):
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
    return articulo

def _obtener_asignacion_existente(db, reserva_id, articulo_id):
    result = db.execute(
        text(
            """
            SELECT cantidad FROM reserva_articulos WHERE
            reserva_id = :reserva_id AND articulo_id = :articulo_id
            """
        ),
        {"reserva_id": reserva_id, "articulo_id": articulo_id}
    ).fetchone()
    return result[0] if result else 0

def _validar_stock(nueva_cantidad, articulo, total_reservado_otras,
                   cantidad_ya_asignada, cantidad, modo):
    disponible = articulo.cantidad - total_reservado_otras + cantidad_ya_asignada
    if nueva_cantidad > disponible:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"No hay suficiente cantidad disponible. "
                f"Ya asignado en esta reserva: {cantidad_ya_asignada}, "
                f"{'Quieres establecer' if modo == 'reemplazar' else 'Quieres agregar'}: "
                f"{cantidad}, "
                f"Total necesario: {nueva_cantidad}, Disponible: {disponible} "
                f"(Stock total: {articulo.cantidad}, Reservado en otras: {total_reservado_otras})"
            ),
        )

def _calcular_total_reservado_otras(db, reserva_id, articulo_id):
    result = db.execute(
        text(
            """
            SELECT SUM(ra.cantidad) FROM reserva_articulos ra
            JOIN reservas r ON ra.reserva_id = r.id
            WHERE ra.articulo_id = :articulo_id
            AND ra.reserva_id != :reserva_id
            AND r.fecha_hora_fin >= NOW()
            """
        ),
        {"articulo_id": articulo_id, "reserva_id": reserva_id}
    ).fetchone()
    return result[0] if result and result[0] else 0

def _insertar_o_actualizar_articulo(db, reserva_id, articulo_id,
                                    cantidad, modo, cantidad_ya_asignada,
                                    articulo, total_reservado_otras):
    if cantidad_ya_asignada:
        nueva_cantidad = cantidad if modo == "reemplazar" else cantidad_ya_asignada + cantidad
        _validar_stock(nueva_cantidad, articulo,
                       total_reservado_otras, cantidad_ya_asignada, cantidad, modo)
        db.execute(
            text(
                """
            UPDATE reserva_articulos
            SET cantidad = :nueva_cantidad
            WHERE reserva_id = :reserva_id
            AND articulo_id = :articulo_id
            """
            ),
            {
                "reserva_id": reserva_id,
                "articulo_id": articulo_id,
                "nueva_cantidad": nueva_cantidad,
            },
        )
    else:
        cantidad_disponible_para_agregar = articulo.cantidad - total_reservado_otras
        if cantidad > cantidad_disponible_para_agregar:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No hay suficiente cantidad disponible. Solicitado: "
                f"{cantidad}, Disponible: {cantidad_disponible_para_agregar}"
                f" (Stock total: {articulo.cantidad}, Reservado en otras: {total_reservado_otras})",
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


# Endpoints de la API para el modelo Reserva.
# Este módulo define los endpoints REST para las operaciones CRUD
# del modelo Reserva utilizando FastAPI.

MAX_LIMIT = 100

router = APIRouter(prefix="/reservas", tags=["reservas"])


@router.post(
    "/",
    response_model=Reserva,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva reserva",
    description="Crear una reserva de sala o artículo con validación automática",
)
def create_reserva(
    reserva_data: ReservaCreate,
    db: Session = Depends(get_db),
    current_user: PersonaModel = Depends(get_current_user),
):
    """Crear nueva reserva de artículo o sala. Valida disponibilidad y detecta conflictos."""
    # Permitir que solo admin cree reservas para terceros
    if not current_user.is_admin and reserva_data.id_persona != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes crear reservas para otra persona",
        )
    try:
        return ReservaService.create_reserva(db, reserva_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.get("/", response_model=List[Reserva])
def get_reservas(
    skip: int = 0,
    limit: int = MAX_LIMIT,
    db: Session = Depends(get_db),
    current_user: PersonaModel = Depends(get_current_user),
):
    """Obtener lista de reservas con paginación.

    - Admin: ve todas las reservas
    - No admin: solo ve sus propias reservas
    """
    if limit > MAX_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El límite máximo es {MAX_LIMIT} registros",
        )

    if current_user.is_admin:
        return ReservaService.get_reservas(db, skip, limit)
    else:
        return ReservaService.get_reservas_by_persona(
            db, current_user.id, skip, limit
        )


@router.get("/{reserva_id}", response_model=Reserva)
def get_reserva(
    reserva_id: int,
    db: Session = Depends(get_db),
    current_user: PersonaModel = Depends(get_current_user),
):
    """Obtener una reserva específica por ID.

    - Admin: puede ver cualquier reserva
    - No admin: solo puede ver sus reservas
    """
    reserva = ReservaService.get_reserva_by_id(db, reserva_id)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una reserva con ID {reserva_id}",
        )
    if not current_user.is_admin and reserva.id_persona != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver esta reserva",
        )
    return reserva


@router.get("/persona/{persona_id}", response_model=List[Reserva])
def get_reservas_by_persona(
    persona_id: int, skip: int = 0, limit: int = MAX_LIMIT, db: Session = Depends(get_db)
):
    """Obtener reservas de una persona específica."""
    if limit > MAX_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El límite máximo es {MAX_LIMIT} registros",
        )

    return ReservaService.get_reservas_by_persona(db, persona_id, skip, limit)


@router.get("/sala/{sala_id}", response_model=List[Reserva])
def get_reservas_by_sala(
    sala_id: int, skip: int = 0, limit: int = MAX_LIMIT, db: Session = Depends(get_db)
):
    """Obtener reservas de una sala específica."""
    if limit > MAX_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El límite máximo es {MAX_LIMIT} registros",
        )

    return ReservaService.get_reservas_by_sala(db, sala_id, skip, limit)


@router.get("/articulo/{articulo_id}", response_model=List[Reserva])
def get_reservas_by_articulo(
    articulo_id: int, skip: int = 0, limit: int = MAX_LIMIT, db: Session = Depends(get_db)
):
    """Obtener reservas de un artículo específico."""
    if limit > MAX_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El límite máximo es {MAX_LIMIT} registros",
        )

    return ReservaService.get_reservas_by_articulo(db, articulo_id, skip, limit)


@router.get("/fechas/rango", response_model=List[Reserva])
def get_reservas_by_fecha_range(
    fecha_inicio: datetime = Query(..., description="Fecha y hora de inicio del rango"),
    fecha_fin: Optional[datetime] = Query(
        None, description="Fecha y hora de fin del rango"
    ),
    skip: int = 0,
    limit: int = MAX_LIMIT,
    db: Session = Depends(get_db),
):
    """Obtener reservas en un rango de fechas."""
    if limit > MAX_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El límite máximo es {MAX_LIMIT} registros",
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
    reserva_id: int,
    reserva_data: ReservaUpdate,
    db: Session = Depends(get_db),
    current_user: PersonaModel = Depends(get_current_user),
):
    """Actualizar una reserva existente.

    - Admin: puede modificar cualquier reserva
    - No admin: solo puede modificar sus reservas
    """
    # Asegurar que el usuario tenga permisos sobre la reserva
    existing = ReservaService.get_reserva_by_id(db, reserva_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una reserva con ID {reserva_id}",
        )
    if not current_user.is_admin and existing.id_persona != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para modificar esta reserva",
        )
    try:
        reserva = ReservaService.update_reserva(db, reserva_id, reserva_data)
        if not reserva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró una reserva con ID {reserva_id}",
            )
        return reserva
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.delete("/{reserva_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reserva(
    reserva_id: int,
    db: Session = Depends(get_db),
    current_user: PersonaModel = Depends(get_current_user),
):
    """Eliminar una reserva del sistema.

    - Admin: puede eliminar cualquier reserva
    - No admin: solo puede eliminar sus reservas
    """
    existing = ReservaService.get_reserva_by_id(db, reserva_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una reserva con ID {reserva_id}",
        )
    if not current_user.is_admin and existing.id_persona != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar esta reserva",
        )

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
def get_articulos_reserva(
    reserva_id: int,
    db: Session = Depends(get_db),
    current_user: PersonaModel = Depends(get_current_user),
):
    """Obtener artículos asignados a una reserva de sala.

    - Admin: puede ver artículos de cualquier reserva
    - No admin: solo puede ver artículos de sus reservas
    """
    reserva = ReservaService.get_reserva_by_id(db, reserva_id)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una reserva con ID {reserva_id}",
        )
    if not current_user.is_admin and reserva.id_persona != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver los artículos de esta reserva",
        )
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
    current_user: PersonaModel = Depends(get_current_user),
):
    """Agregar o actualizar artículo en una reserva de sala.

    - Admin: puede gestionar artículos de cualquier reserva
    - No admin: solo puede gestionar artículos de sus reservas
    """
    reserva = _verificar_reserva_existente(db, reserva_id)
    _verificar_permiso_modificar_reserva(reserva, current_user)
    _verificar_reserva_es_sala(reserva)
    articulo = _verificar_articulo_existente(db, articulo_id)
    cantidad_ya_asignada = _obtener_asignacion_existente(db, reserva_id, articulo_id)
    total_reservado_otras = _calcular_total_reservado_otras(db, reserva_id, articulo_id)
    _insertar_o_actualizar_articulo(db, reserva_id, articulo_id,
                                    cantidad, modo, cantidad_ya_asignada,
                                    articulo, total_reservado_otras)
    db.commit()
    return {"message": "Artículo agregado a la reserva exitosamente"}


@router.delete("/{reserva_id}/articulos/{articulo_id}")
def remove_articulo_from_reserva(
    reserva_id: int,
    articulo_id: int,
    db: Session = Depends(get_db),
    current_user: PersonaModel = Depends(get_current_user),
):
    """Eliminar un artículo de una reserva de sala.

    - Admin: puede gestionar artículos de cualquier reserva
    - No admin: solo puede gestionar artículos de sus reservas
    """
    reserva = ReservaService.get_reserva_by_id(db, reserva_id)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una reserva con ID {reserva_id}",
        )
    if not current_user.is_admin and reserva.id_persona != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para modificar los artículos de esta reserva",
        )
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

    # Determinar si alguna fila fue afectada (compatibilidad con SQLAlchemy)
    rowcount = getattr(result, "rowcount", None)
    if rowcount is None:
        # Fallback simple: verificar si aún existe el vínculo
        verify = db.execute(
            text(
                """
            SELECT 1 FROM reserva_articulos
            WHERE reserva_id = :reserva_id AND articulo_id = :articulo_id
            LIMIT 1
            """
            ),
            {"reserva_id": reserva_id, "articulo_id": articulo_id},
        ).fetchone()
        if verify is not None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró el artículo en la reserva",
            )
    elif rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró el artículo en la reserva",
        )

    return {"message": "Artículo eliminado de la reserva exitosamente"}
