"""
Endpoints de la API para el modelo Articulo.

Este módulo define los endpoints REST para las operaciones CRUD
del modelo Articulo utilizando FastAPI.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.articulo import Articulo, ArticuloCreate, ArticuloUpdate
from app.services.articulo_service import ArticuloService

router = APIRouter(prefix="/articulos", tags=["articulos"])


@router.post("/", response_model=Articulo, status_code=status.HTTP_201_CREATED)
def create_articulo(articulo_data: ArticuloCreate, db: Session = Depends(get_db)):
    """Crear un nuevo artículo."""
    return ArticuloService.create_articulo(db, articulo_data)


@router.get("/", response_model=List[Articulo])
def get_articulos(
    skip: int = 0,
    limit: int = 100,
    disponible: Optional[bool] = Query(None, description="Filtrar por disponibilidad"),
    db: Session = Depends(get_db),
):
    """Obtener lista de artículos con filtros opcionales."""
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El límite máximo es 100 registros",
        )

    return ArticuloService.get_articulos(db, skip, limit, disponible)


@router.get("/disponibles", response_model=List[Articulo])
def get_articulos_disponibles(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener artículos disponibles."""
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El límite máximo es 100 registros",
        )

    return ArticuloService.get_articulos_disponibles(db, skip, limit)


@router.get("/disponibilidad")
def get_disponibilidad_articulos(
    fecha_inicio: str,
    fecha_fin: str,
    reserva_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """Obtener disponibilidad de artículos para un período específico."""
    from datetime import datetime

    try:
        fecha_inicio_dt = datetime.fromisoformat(fecha_inicio.replace("Z", "+00:00"))
        fecha_fin_dt = datetime.fromisoformat(fecha_fin.replace("Z", "+00:00"))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de fecha inválido. Use formato ISO (YYYY-MM-DDTHH:MM:SS)",
        )

    # Obtener todos los artículos disponibles
    articulos = ArticuloService.get_articulos(db, skip=0, limit=1000)

    resultado = []

    for articulo in articulos:
        if not articulo.disponible:
            continue

        # Calcular cantidad reservada en el período
        query = text(
            """
            SELECT COALESCE(SUM(cantidad_usada), 0) as total_reservado
            FROM (
                -- Reservas directas del artículo
                SELECT 1 as cantidad_usada
                FROM reservas r
                WHERE r.id_articulo = :articulo_id
                AND (:reserva_id IS NULL OR r.id != :reserva_id)
                AND r.fecha_hora_fin >= :fecha_inicio
                AND r.fecha_hora_inicio <= :fecha_fin

                UNION ALL

                -- Artículos en reservas de sala
                SELECT ra.cantidad as cantidad_usada
                FROM reserva_articulos ra
                JOIN reservas r ON ra.reserva_id = r.id
                WHERE ra.articulo_id = :articulo_id
                AND (:reserva_id IS NULL OR ra.reserva_id != :reserva_id)
                AND r.fecha_hora_fin >= :fecha_inicio
                AND r.fecha_hora_inicio <= :fecha_fin
            ) as reservas_activas
        """
        )

        result = db.execute(
            query,
            {
                "articulo_id": articulo.id,
                "reserva_id": reserva_id,
                "fecha_inicio": fecha_inicio_dt,
                "fecha_fin": fecha_fin_dt,
            },
        )

        total_reservado_otras = result.scalar() or 0

        # Calcular cuánto ya tiene asignado esta reserva (si aplica)
        ya_asignada_en_reserva = 0
        if reserva_id is not None:
            result_mia = db.execute(
                text(
                    """
                    SELECT COALESCE(SUM(ra.cantidad), 0) as total
                    FROM reserva_articulos ra
                    WHERE ra.articulo_id = :articulo_id
                    AND ra.reserva_id = :reserva_id
                    """
                ),
                {"articulo_id": articulo.id, "reserva_id": reserva_id},
            )
            ya_asignada_en_reserva = result_mia.scalar() or 0

        # Disponible total ignorando esta reserva (para compatibilidad)
        disponible = max(0, articulo.cantidad - total_reservado_otras)
        # Disponible para agregar (ya descontando lo asignado en esta reserva)
        disponible_para_agregar = max(
            0, articulo.cantidad - total_reservado_otras - ya_asignada_en_reserva
        )

        resultado.append(
            {
                "id": articulo.id,
                "nombre": articulo.nombre,
                "descripcion": articulo.descripcion,
                "categoria": articulo.categoria,
                "cantidad_total": articulo.cantidad,
                # Para compatibilidad: lo reservado por otros (excluye esta reserva)
                "cantidad_reservada_otros": total_reservado_otras,
                # Lo que ya tiene asignado esta reserva
                "cantidad_asignada_en_reserva": ya_asignada_en_reserva,
                # Disponible total ignorando esta reserva (mantener campo histórico)
                "cantidad_disponible": disponible,
                # NUEVO: lo que realmente puede agregar adicionalmente en esta reserva
                "cantidad_disponible_para_agregar": disponible_para_agregar,
            }
        )

    return resultado


@router.get("/estadisticas/inventario")
def get_estadisticas_inventario(db: Session = Depends(get_db)):
    """
    Obtener estadísticas generales del inventario.

    Retorna:
    - total_articulos: Cantidad de tipos de artículos diferentes
    - total_unidades: Suma de todas las unidades disponibles en stock
    - unidades_reservadas: Unidades reservadas en reservas activas en este momento
    - unidades_disponibles: Unidades que se pueden reservar ahora
    - articulos_disponibles: Artículos marcados como disponibles
    - articulos_no_disponibles: Artículos marcados como no disponibles

    Nota: Las unidades reservadas solo incluyen las reservas que están activas EN ESTE MOMENTO
    (fecha_hora_inicio <= ahora <= fecha_hora_fin). Las reservas futuras no se cuentan.
    """
    from datetime import datetime

    # Obtener todos los artículos usando el servicio
    articulos = ArticuloService.get_articulos(db, 0, 1000)

    total_articulos = len(articulos)
    total_unidades = sum(art.cantidad for art in articulos)
    articulos_disponibles = sum(1 for art in articulos if art.disponible)
    articulos_no_disponibles = total_articulos - articulos_disponibles

    # Calcular unidades reservadas actualmente (en curso ahora)
    ahora = datetime.now()
    query_reservadas = text(
        """
        SELECT COALESCE(SUM(cantidad_usada), 0) as total
        FROM (
            -- Reservas directas de artículos (activas ahora)
            SELECT 1 as cantidad_usada
            FROM reservas r
            WHERE r.id_articulo IS NOT NULL
            AND r.fecha_hora_fin >= :ahora
            AND r.fecha_hora_inicio <= :ahora

            UNION ALL

            -- Artículos en reservas de sala (activas ahora)
            SELECT ra.cantidad as cantidad_usada
            FROM reserva_articulos ra
            JOIN reservas r ON ra.reserva_id = r.id
            WHERE r.fecha_hora_fin >= :ahora
            AND r.fecha_hora_inicio <= :ahora
        ) as reservas_activas
    """
    )

    result = db.execute(query_reservadas, {"ahora": ahora})
    unidades_reservadas = result.scalar() or 0
    unidades_disponibles = max(0, total_unidades - unidades_reservadas)

    return {
        "total_articulos": total_articulos,
        "articulos_disponibles": articulos_disponibles,
        "articulos_no_disponibles": articulos_no_disponibles,
        "total_unidades": total_unidades,
        "unidades_reservadas": unidades_reservadas,
        "unidades_disponibles": unidades_disponibles,
    }


@router.get("/disponibilidad/actual")
def get_disponibilidad_actual_articulos(db: Session = Depends(get_db)):
    """Obtener disponibilidad actual de todos los artículos."""
    from datetime import datetime

    # Obtener todos los artículos
    articulos = ArticuloService.get_articulos(db, 0, 1000)
    ahora = datetime.now()

    disponibilidad = {}

    for articulo in articulos:
        # Calcular unidades reservadas ahora para este artículo
        query_reservadas = text(
            """
            SELECT COALESCE(SUM(cantidad_usada), 0) as total
            FROM (
                -- Reservas directas del artículo (activas ahora)
                SELECT 1 as cantidad_usada
                FROM reservas r
                WHERE r.id_articulo = :articulo_id
                AND r.fecha_hora_fin >= :ahora
                AND r.fecha_hora_inicio <= :ahora

                UNION ALL

                -- Artículos en reservas de sala (activas ahora)
                SELECT ra.cantidad as cantidad_usada
                FROM reserva_articulos ra
                JOIN reservas r ON ra.reserva_id = r.id
                WHERE ra.articulo_id = :articulo_id
                AND r.fecha_hora_fin >= :ahora
                AND r.fecha_hora_inicio <= :ahora
            ) as reservas_activas
        """
        )

        result = db.execute(
            query_reservadas, {"articulo_id": articulo.id, "ahora": ahora}
        )
        unidades_reservadas = result.scalar() or 0
        unidades_disponibles = max(0, articulo.cantidad - unidades_reservadas)

        disponibilidad[articulo.id] = {
            "total": articulo.cantidad,
            "reservadas": unidades_reservadas,
            "disponibles": unidades_disponibles,
        }

    return disponibilidad


@router.get("/{articulo_id}", response_model=Articulo)
def get_articulo(articulo_id: int, db: Session = Depends(get_db)):
    """Obtener un artículo específico por ID."""
    articulo = ArticuloService.get_articulo_by_id(db, articulo_id)
    if not articulo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un artículo con ID {articulo_id}",
        )
    return articulo


@router.put("/{articulo_id}", response_model=Articulo)
def update_articulo(
    articulo_id: int, articulo_data: ArticuloUpdate, db: Session = Depends(get_db)
):
    """Actualizar datos de un artículo existente."""
    articulo = ArticuloService.update_articulo(db, articulo_id, articulo_data)
    if not articulo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un artículo con ID {articulo_id}",
        )
    return articulo


@router.patch("/{articulo_id}/toggle-disponibilidad", response_model=Articulo)
def toggle_disponibilidad(articulo_id: int, db: Session = Depends(get_db)):
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
            detail=f"No se encontró un artículo con ID {articulo_id}",
        )
    return articulo


@router.delete("/{articulo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_articulo(articulo_id: int, db: Session = Depends(get_db)):
    """Eliminar un artículo del sistema."""
    try:
        success = ArticuloService.delete_articulo(db, articulo_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró un artículo con ID {articulo_id}",
            )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/count/total")
def count_articulos(
    disponible: Optional[bool] = Query(
        None, description="Filtrar conteo por disponibilidad"
    ),
    db: Session = Depends(get_db),
):
    """Obtener el número total de artículos."""
    count = ArticuloService.count_articulos(db, disponible)
    return {"total": count, "disponible": disponible}


@router.get("/{articulo_id}/reservas")
def get_reservas_articulo(articulo_id: int, db: Session = Depends(get_db)):
    """Obtener reservas activas y futuras donde se usa este artículo."""
    # Reservas directas del artículo
    result_directas = db.execute(
        text(
            """
        SELECT r.id, r.id_persona, r.fecha_hora_inicio, r.fecha_hora_fin,
               p.nombre as persona_nombre, 'directo' as tipo
        FROM reservas r
        JOIN personas p ON r.id_persona = p.id
        WHERE r.id_articulo = :articulo_id
        AND r.fecha_hora_fin >= NOW()
        ORDER BY r.fecha_hora_inicio
        """
        ),
        {"articulo_id": articulo_id},
    )

    # Reservas de salas que requieren el artículo
    result_salas = db.execute(
        text(
            """
        SELECT r.id, r.id_persona, r.fecha_hora_inicio, r.fecha_hora_fin,
               p.nombre as persona_nombre, s.nombre as sala_nombre,
               ra.cantidad, 'sala' as tipo
        FROM reserva_articulos ra
        JOIN reservas r ON ra.reserva_id = r.id
        JOIN personas p ON r.id_persona = p.id
        JOIN salas s ON r.id_sala = s.id
        WHERE ra.articulo_id = :articulo_id
        AND r.fecha_hora_fin >= NOW()
        ORDER BY r.fecha_hora_inicio
        """
        ),
        {"articulo_id": articulo_id},
    )

    reservas = []

    # Procesar reservas directas
    for row in result_directas:
        reservas.append(
            {
                "id": row[0],
                "id_persona": row[1],
                "fecha_hora_inicio": row[2].isoformat() if row[2] else None,
                "fecha_hora_fin": row[3].isoformat() if row[3] else None,
                "persona_nombre": row[4],
                "tipo": "Reserva Directa",
                "cantidad": 1,
            }
        )

    # Procesar reservas de salas
    for row in result_salas:
        reservas.append(
            {
                "id": row[0],
                "id_persona": row[1],
                "fecha_hora_inicio": row[2].isoformat() if row[2] else None,
                "fecha_hora_fin": row[3].isoformat() if row[3] else None,
                "persona_nombre": row[4],
                "sala_nombre": row[5],
                "cantidad": row[6],
                "tipo": "Reserva de Sala",
            }
        )

    return reservas
