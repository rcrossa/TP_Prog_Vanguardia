
"""
Endpoints de la API para el modelo Articulo.

Este módulo define los endpoints REST para las operaciones CRUD
del modelo Articulo utilizando FastAPI.
"""
from datetime import datetime
from typing import List, Optional
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.articulo import Articulo, ArticuloCreate, ArticuloUpdate
from app.services.java_client import JavaServiceClient
from app.services.articulo_service import ArticuloService

router = APIRouter(prefix="/articulos", tags=["articulos"])


@router.post("/", response_model=Articulo, status_code=status.HTTP_201_CREATED)
async def create_articulo(articulo_data: ArticuloCreate):
    """Crear un nuevo artículo directamente en el microservicio Java."""
    java_payload = articulo_data.model_dump()
    result = await JavaServiceClient.create_articulo(java_payload)
    if result is None:
        return JSONResponse(
            status_code=503,
            content={"detail": "No se pudo crear el artículo en el servicio Java."}
        )
    return result


@router.get("/", response_model=List[Articulo])
async def get_articulos():
    """Obtener lista de artículos directamente desde el microservicio Java."""
    articulos = await JavaServiceClient.get_articulos()
    if articulos is None:
        return JSONResponse(
            status_code=503,
            content={"detail": "No se pudo obtener la lista de artículos desde el servicio Java."}
        )
    return articulos


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

    try:
        fecha_inicio_dt = datetime.fromisoformat(fecha_inicio.replace("Z", "+00:00"))
        fecha_fin_dt = datetime.fromisoformat(fecha_fin.replace("Z", "+00:00"))
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de fecha inválido. Use formato ISO (YYYY-MM-DDTHH:MM:SS)",
        ) from exc

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

    # Obtener todos los artículos usando el servicio
    articulos = ArticuloService.get_articulos(db, 0, 1000)

    total_articulos = len(articulos)
    total_unidades = sum(art.cantidad for art in articulos)
    articulos_disponibles = sum(1 for art in articulos if art.disponible)
    articulos_no_disponibles = total_articulos - articulos_disponibles

    # Calcular unidades reservadas actualmente (en curso ahora)
    # Las fechas en la BD son "naive" (sin timezone), representan hora local ART (UTC-3)
    # Ajustamos la hora actual restando 3 horas para comparar con fechas locales
    query_reservadas = text(
        """
        SELECT COALESCE(SUM(cantidad_usada), 0) as total
        FROM (
            -- Reservas directas de artículos (activas ahora en hora local)
            SELECT 1 as cantidad_usada
            FROM reservas r
            WHERE r.id_articulo IS NOT NULL
            AND r.fecha_hora_fin >= (CURRENT_TIMESTAMP - INTERVAL '3 hours')
            AND r.fecha_hora_inicio <= (CURRENT_TIMESTAMP - INTERVAL '3 hours')

            UNION ALL

            -- Artículos en reservas de sala (activas ahora en hora local)
            SELECT ra.cantidad as cantidad_usada
            FROM reserva_articulos ra
            JOIN reservas r ON ra.reserva_id = r.id
            WHERE r.fecha_hora_fin >= (CURRENT_TIMESTAMP - INTERVAL '3 hours')
            AND r.fecha_hora_inicio <= (CURRENT_TIMESTAMP - INTERVAL '3 hours')
        ) as reservas_activas
    """
    )

    result = db.execute(query_reservadas)
    unidades_reservadas = result.scalar() or 0
    unidades_disponibles = max(0, total_unidades - unidades_reservadas)

    # Calcular cuántos artículos tienen stock completamente agotado HOY
    # Necesitamos encontrar artículos donde en ALGÚN MOMENTO del día,
    # todas las unidades están reservadas simultáneamente
    query_articulos_sin_stock = text(
        """
        WITH reservas_hoy AS (
            -- Todas las reservas que tocan el día de hoy (hora local)
            SELECT DISTINCT r.id, r.fecha_hora_inicio, r.fecha_hora_fin
            FROM reservas r
            WHERE r.fecha_hora_fin >= DATE_TRUNC('day', CURRENT_TIMESTAMP - INTERVAL '3 hours')
            AND r.fecha_hora_inicio <= DATE_TRUNC('day', CURRENT_TIMESTAMP - INTERVAL '3 hours') + INTERVAL '1 day' - INTERVAL '1 second'
        ),
        articulos_en_reservas AS (
            -- Para cada artículo, encontrar el máximo de unidades reservadas simultáneamente
            SELECT 
                a.id as articulo_id,
                a.cantidad as stock_total,
                (
                    SELECT MAX(total_en_momento)
                    FROM (
                        -- Para cada reserva, contar cuántas unidades del artículo están reservadas
                        -- en reservas que se solapan con esta
                        SELECT r1.id as reserva_id, COALESCE(SUM(
                            CASE 
                                WHEN ra.articulo_id = a.id THEN ra.cantidad
                                ELSE 0
                            END
                        ), 0) as total_en_momento
                        FROM reservas_hoy r1
                        LEFT JOIN reservas r2 ON (
                            r2.fecha_hora_inicio <= r1.fecha_hora_fin
                            AND r2.fecha_hora_fin >= r1.fecha_hora_inicio
                        )
                        LEFT JOIN reserva_articulos ra ON ra.reserva_id = r2.id
                        GROUP BY r1.id
                    ) as momentos
                ) as max_reservado_simultaneo
            FROM articulos a
        )
        SELECT COUNT(*) as total
        FROM articulos_en_reservas
        WHERE stock_total <= max_reservado_simultaneo
    """
    )

    result_sin_stock = db.execute(query_articulos_sin_stock)
    articulos_sin_stock_ahora = result_sin_stock.scalar() or 0

    return {
        "total_articulos": total_articulos,
        "articulos_disponibles": articulos_disponibles,
        "articulos_no_disponibles": articulos_no_disponibles,
        "articulos_sin_stock_ahora": articulos_sin_stock_ahora,  # NUEVO: artículos con 0 unidades disponibles
        "total_unidades": total_unidades,
        "unidades_reservadas": unidades_reservadas,
        "unidades_disponibles": unidades_disponibles,
    }


@router.get("/disponibilidad/actual")
def get_disponibilidad_actual_articulos(db: Session = Depends(get_db)):
    """Obtener disponibilidad actual de todos los artículos."""

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
async def get_articulo(articulo_id: int):
    """Obtener un artículo específico por ID desde el microservicio Java."""
    result = await JavaServiceClient.get_articulo(articulo_id)
    if result is None:
        return JSONResponse(
            status_code=404,
            content={
                "detail": f"No se encontró un artículo con ID {articulo_id} en el servicio Java."
                }
        )
    return result


@router.put("/{articulo_id}", response_model=Articulo)
async def update_articulo(articulo_id: int, articulo_data: ArticuloUpdate):
    """Actualizar datos de un artículo directamente en el microservicio Java."""
    # Obtener el artículo actual desde Java para rellenar campos faltantes
    articulo_actual = await JavaServiceClient.get_articulo(articulo_id)
    if articulo_actual is None:
        return JSONResponse(
            status_code=404,
            content={"detail":
                     f"No se encontró un artículo con ID {articulo_id} en el servicio Java."}
        )

    data_dict = articulo_data.model_dump(exclude_unset=True)
    payload = {
        "nombre": data_dict.get("nombre", articulo_actual.get("nombre")),
        "descripcion": data_dict.get("descripcion", articulo_actual.get("descripcion")),
        "cantidad": data_dict.get("cantidad", articulo_actual.get("cantidad", 1)),
        "categoria": data_dict.get("categoria", articulo_actual.get("categoria")),
        "disponible": data_dict.get("disponible", articulo_actual.get("disponible", True)),
    }

    result = await JavaServiceClient.update_articulo(articulo_id, payload)
    if result is None:
        return JSONResponse(
            status_code=404,
            content={
                "detail": (
                    f"No se encontró un artículo con ID {articulo_id} en el servicio Java."
                )
            }
        )
    return result


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
            detail=(
                f"No se encontró un artículo con ID {articulo_id}"
            ),
        )
    return articulo


@router.delete("/{articulo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_articulo(articulo_id: int):
    """Eliminar un artículo directamente en el microservicio Java."""
    result = await JavaServiceClient.delete_articulo(articulo_id)
    if not result:
        return JSONResponse(
            status_code=404,
            content={
                "detail": (
                    f"No se encontró un artículo con ID {articulo_id} en el servicio Java."
                )
            }
        )
    return JSONResponse(status_code=204, content={})


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
    # Mostrar la URL de conexión y la base activa
    try:
        result_dbname = db.execute(text("SELECT current_database()"))
        dbname = result_dbname.scalar()
        print(f"[DEBUG] current_database: {dbname}")
    except Exception as e:
        print(f"[DEBUG] error mostrando info de conexión: {e}")
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
        ORDER BY r.fecha_hora_inicio
        """
        ),
        {"articulo_id": articulo_id},
    )

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
        ORDER BY r.fecha_hora_inicio
        """
        ),
        {"articulo_id": articulo_id},
    )

    directas_list = list(result_directas)
    salas_list = list(result_salas)
    reservas = []
    for row in directas_list:
        reservas.append({
            "id": row[0],
            "id_persona": row[1],
            "fecha_hora_inicio": row[2].isoformat() if row[2] else None,
            "fecha_hora_fin": row[3].isoformat() if row[3] else None,
            "persona_nombre": row[4],
            "tipo": "Reserva Directa",
            "cantidad": 1,
        })
    for row in salas_list:
        reservas.append({
            "id": row[0],
            "id_persona": row[1],
            "fecha_hora_inicio": row[2].isoformat() if row[2] else None,
            "fecha_hora_fin": row[3].isoformat() if row[3] else None,
            "persona_nombre": row[4],
            "sala_nombre": row[5],
            "cantidad": row[6],
            "tipo": "Reserva de Sala",
        })
    return reservas
