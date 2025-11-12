

"""
Servicio para operaciones de negocio de Reserva.

Este módulo contiene la lógica de negocio para el modelo Reserva,
incluyendo validaciones complejas y operaciones de reservas.
"""
import logging
from datetime import datetime, timedelta
from typing import List, Optional
import asyncio
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.models.reserva import Reserva
from app.repositories.reserva_repository import ReservaRepository
from app.schemas.reserva import ReservaCreate, ReservaUpdate
from app.services.java_client import JavaServiceClient
from app.services.persona_service import PersonaService
from app.repositories.articulo_repository import ArticuloRepository

logger = logging.getLogger(__name__)


class ReservaService:
    """Servicio para operaciones de negocio de Reserva."""

    @staticmethod
    def create_reserva(db: Session, reserva_data: ReservaCreate) -> Reserva:
        """
        Crear una nueva reserva con validaciones completas.

        Args:
            db: Sesión de base de datos
            reserva_data: Datos para crear la reserva

        Returns:
            Reserva creada

        Raises:
            ValueError: Si hay errores de validación o conflictos
        """
        # Validar que la persona existe
        if not PersonaService.validate_persona_exists(db, reserva_data.id_persona):
            raise ValueError(f"No existe una persona con ID "
                             f"{reserva_data.id_persona}")

        # Validar fechas
        if reserva_data.fecha_hora_fin <= reserva_data.fecha_hora_inicio:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")

        # Validar que no se está reservando demasiado en el pasado
        # Permitir un margen de 30 minutos para compensar desfases de tiempo y casos de uso reales
        now = datetime.now()
        margin_minutes = 30
        cutoff_time = now - timedelta(minutes=margin_minutes)

        if reserva_data.fecha_hora_inicio < cutoff_time:
            raise ValueError(
                f"No se pueden crear reservas con más de {margin_minutes} minutos en el pasado"
            )

        # Una reserva debe ser para un artículo O una sala, no ambos ni ninguno
        has_articulo = reserva_data.id_articulo is not None
        has_sala = reserva_data.id_sala is not None

        if not has_articulo and not has_sala:
            raise ValueError("La reserva debe ser para un artículo o una sala")

        if has_articulo and has_sala:
            raise ValueError(
                "La reserva no puede ser para un artículo y una sala al mismo tiempo"
            )

        # Validaciones específicas según el tipo de reserva
        if has_articulo:
            ReservaService._validate_articulo_reservation(db, reserva_data)

        if has_sala:
            ReservaService._validate_sala_reservation(db, reserva_data)

        return ReservaRepository.create(db, reserva_data)

    @staticmethod
    def _validate_articulo_reservation(db: Session, reserva_data: ReservaCreate) -> None:
        """
        Validar reserva de artículo SOLO si el servicio Java está disponible.
        Si el servicio Java no responde, se muestra un error claro y no se permite la reserva.
        """
        if reserva_data.id_articulo is None:
            return

    # ...existing code...
        # Verificar disponibilidad del servicio Java
        is_java_up = asyncio.run(JavaServiceClient.check_service_health())
        if not is_java_up:
            raise ValueError(
                "El sistema de gestión de artículos no está disponible en este momento. "
                "Por favor, intente más tarde."
            )
        # Validar existencia y disponibilidad del artículo en Java
        java_validation = asyncio.run(
            JavaServiceClient.validate_articulo_exists(reserva_data.id_articulo))
        if not java_validation:
            raise ValueError(
                f"El artículo con ID {reserva_data.id_articulo} "
                f"no existe en el sistema de gestión de artículos."
            )
        # Obtener el artículo para verificar la cantidad total (local)
        articulo = ArticuloRepository.get_by_id(db, reserva_data.id_articulo)
        if not articulo:
            raise ValueError(
                f"El artículo con ID {reserva_data.id_articulo} no existe"
            )
        # Calcular cuántas unidades están reservadas en el mismo período
        result = db.execute(
            text(
                """
                SELECT COALESCE(SUM(cantidad_usada), 0) as total_reservado
                FROM (
                    SELECT 1 as cantidad_usada
                    FROM reservas r
                    WHERE r.id_articulo = :articulo_id
                    AND r.fecha_hora_fin >= :fecha_inicio
                    AND r.fecha_hora_inicio <= :fecha_fin
                    UNION ALL
                    SELECT ra.cantidad as cantidad_usada
                    FROM reserva_articulos ra
                    JOIN reservas r ON ra.reserva_id = r.id
                    WHERE ra.articulo_id = :articulo_id
                    AND r.fecha_hora_fin >= :fecha_inicio
                    AND r.fecha_hora_inicio <= :fecha_fin
                ) as reservas_activas
                """
            ),
            {
                "articulo_id": reserva_data.id_articulo,
                "fecha_inicio": reserva_data.fecha_hora_inicio,
                "fecha_fin": reserva_data.fecha_hora_fin,
            },
        )
        total_reservado = result.scalar() or 0
        cantidad_disponible = articulo.cantidad - total_reservado
        if cantidad_disponible < 1:
            raise ValueError(
                f"No hay unidades disponibles del artículo '{articulo.nombre}' "
                f"en el período solicitado. "
                f"Total: {articulo.cantidad}, "
                f"Ya reservado: {total_reservado}"
            )

    @staticmethod
    def _validate_sala_reservation(db: Session, reserva_data: ReservaCreate) -> None:
        """
        Validar reserva de sala SOLO si el servicio Java está disponible.
        Si el servicio Java no responde, se muestra un error claro y no se permite la reserva.
        """
        if reserva_data.id_sala is None:
            return

    # ...existing code...
        # Verificar disponibilidad del servicio Java
        is_java_up = asyncio.run(JavaServiceClient.check_service_health())
        if not is_java_up:
            raise ValueError(
                "El sistema de gestión de salas no está disponible en este momento. "
                "Por favor, intente más tarde."
            )
        # Validar existencia y disponibilidad de la sala en Java
        java_validation = asyncio.run(JavaServiceClient.validate_sala_exists(reserva_data.id_sala))
        if not java_validation:
            raise ValueError(
                f"La sala con ID {reserva_data.id_sala}"
                f" no existe en el sistema de gestión de salas."
            )
        is_disponible = asyncio.run(JavaServiceClient.check_sala_disponible(reserva_data.id_sala))
        if not is_disponible:
            raise ValueError(
                f"La sala con ID {reserva_data.id_sala} "
                f"no está disponible según el sistema de gestión de salas."
            )
        # Verificar conflictos de horario en la sala (siempre se hace localmente)
        conflicts = ReservaRepository.check_conflicts(
            db,
            reserva_data.id_sala,
            reserva_data.fecha_hora_inicio,
            reserva_data.fecha_hora_fin,
        )
        if conflicts:
            raise ValueError(
                "Ya existe una reserva en la sala para el horario especificado"
            )

    @staticmethod
    def get_reserva_by_id(db: Session, reserva_id: int) -> Optional[Reserva]:
        """
        Obtener una reserva por su ID.

        Args:
            db: Sesión de base de datos
            reserva_id: ID de la reserva

        Returns:
            Reserva encontrada o None
        """
        return ReservaRepository.get_by_id(db, reserva_id)

    @staticmethod
    def get_reservas(db: Session, skip: int = 0, limit: int = 100) -> List[Reserva]:
        """
        Obtener lista de reservas.

        Args:
            db: Sesión de base de datos
            skip: Registros a omitir (paginación)
            limit: Máximo número de registros

        Returns:
            Lista de reservas
        """
        return ReservaRepository.get_all(db, skip, limit)

    @staticmethod
    def get_reservas_by_persona(
        db: Session, persona_id: int, skip: int = 0, limit: int = 100
    ) -> List[Reserva]:
        """
        Obtener reservas de una persona específica.

        Args:
            db: Sesión de base de datos
            persona_id: ID de la persona
            skip: Registros a omitir (paginación)
            limit: Máximo número de registros

        Returns:
            Lista de reservas de la persona
        """
        return ReservaRepository.get_by_persona(db, persona_id, skip, limit)

    @staticmethod
    def get_reservas_by_sala(
        db: Session, sala_id: int, skip: int = 0, limit: int = 100
    ) -> List[Reserva]:
        """
        Obtener reservas de una sala específica.

        Args:
            db: Sesión de base de datos
            sala_id: ID de la sala
            skip: Registros a omitir (paginación)
            limit: Máximo número de registros

        Returns:
            Lista de reservas de la sala
        """
        return ReservaRepository.get_by_sala(db, sala_id, skip, limit)

    @staticmethod
    def get_reservas_by_articulo(
        db: Session, articulo_id: int, skip: int = 0, limit: int = 100
    ) -> List[Reserva]:
        """
        Obtener reservas de un artículo específico.

        Args:
            db: Sesión de base de datos
            articulo_id: ID del artículo
            skip: Registros a omitir (paginación)
            limit: Máximo número de registros

        Returns:
            Lista de reservas del artículo
        """
        return ReservaRepository.get_by_articulo(db, articulo_id, skip, limit)

    @staticmethod
    def get_reservas_by_fecha_range(
        db: Session,
        fecha_inicio: datetime,
        fecha_fin: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Reserva]:
        """
        Obtener reservas en un rango de fechas.

        Args:
            db: Sesión de base de datos
            fecha_inicio: Fecha de inicio del rango
            fecha_fin: Fecha de fin del rango (opcional)
            skip: Registros a omitir (paginación)
            limit: Máximo número de registros

        Returns:
            Lista de reservas en el rango
        """
        return ReservaRepository.get_by_fecha_range(
            db, fecha_inicio, fecha_fin, skip, limit
        )

    @staticmethod
    def update_reserva(
        db: Session, reserva_id: int, reserva_data: ReservaUpdate
    ) -> Optional[Reserva]:
        """
        Actualizar una reserva existente con validaciones.

        Args:
            db: Sesión de base de datos
            reserva_id: ID de la reserva a actualizar
            reserva_data: Nuevos datos de la reserva

        Returns:
            Reserva actualizada o None si no existe

        Raises:
            ValueError: Si hay errores de validación o conflictos
        """
        # Obtener la reserva actual
        current_reserva = ReservaRepository.get_by_id(db, reserva_id)
        if not current_reserva:
            return None

        # Validaciones básicas de fechas si se están actualizando
        fecha_inicio = (
            reserva_data.fecha_hora_inicio
            if reserva_data.fecha_hora_inicio
            else current_reserva.fecha_hora_inicio
        )
        fecha_fin = (
            reserva_data.fecha_hora_fin
            if reserva_data.fecha_hora_fin
            else current_reserva.fecha_hora_fin
        )

        if fecha_fin <= fecha_inicio:
            raise ValueError(
                "La fecha de fin debe ser posterior a la fecha de inicio"
            )

        # Validar que no se está reservando en el pasado
        if fecha_inicio < datetime.now():
            raise ValueError(
                "No se pueden modificar reservas para fechas pasadas"
            )

        # Si se está cambiando el artículo, validar disponibilidad
        if (
            reserva_data.id_articulo is not None
            and reserva_data.id_articulo != current_reserva.id_articulo
        ):
            # Crear objeto temporal para validación


            temp_data = ReservaCreate(
                id_persona=(
                    reserva_data.id_persona
                    if reserva_data.id_persona
                    else current_reserva.id_persona
                ),
                fecha_hora_inicio=fecha_inicio,
                fecha_hora_fin=fecha_fin,
                id_articulo=reserva_data.id_articulo,
                id_sala=None,
            )
            ReservaService._validate_articulo_reservation(db, temp_data)

        # Si se está cambiando la sala, validar conflictos
        if (
            reserva_data.id_sala is not None
            and reserva_data.id_sala != current_reserva.id_sala
        ):

            temp_data = ReservaCreate(
                id_persona=(
                    reserva_data.id_persona
                    if reserva_data.id_persona
                    else current_reserva.id_persona
                ),
                fecha_hora_inicio=fecha_inicio,
                fecha_hora_fin=fecha_fin,
                id_articulo=None,
                id_sala=reserva_data.id_sala,
            )
            ReservaService._validate_sala_reservation(db, temp_data)

        # Si se están cambiando las fechas de una reserva de artículo, validar
        if current_reserva.id_articulo and (
            reserva_data.fecha_hora_inicio or reserva_data.fecha_hora_fin
        ):


            temp_data = ReservaCreate(
                id_persona=(
                    reserva_data.id_persona
                    if reserva_data.id_persona
                    else current_reserva.id_persona
                ),
                fecha_hora_inicio=fecha_inicio,
                fecha_hora_fin=fecha_fin,
                id_articulo=current_reserva.id_articulo,
                id_sala=None,
            )
            # Validar disponibilidad excluyendo la reserva actual

            articulo = ArticuloRepository.get_by_id(db, current_reserva.id_articulo)
            if articulo:
                result = db.execute(
                    text(
                        """
                    SELECT COALESCE(SUM(cantidad_usada), 0) as total_reservado
                    FROM (
                        SELECT 1 as cantidad_usada
                        FROM reservas r
                        WHERE r.id_articulo = :articulo_id
                        AND r.id != :reserva_id
                        AND r.fecha_hora_fin >= :fecha_inicio
                        AND r.fecha_hora_inicio <= :fecha_fin

                        UNION ALL

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
                        "articulo_id": current_reserva.id_articulo,
                        "reserva_id": reserva_id,
                        "fecha_inicio": fecha_inicio,
                        "fecha_fin": fecha_fin,
                    },
                )

                total_reservado = result.scalar() or 0
                cantidad_disponible = articulo.cantidad - total_reservado

                if cantidad_disponible < 1:
                    raise ValueError(
                        f"No hay unidades disponibles del artículo '{articulo.nombre}' "
                        f"en el nuevo período. "
                        f"Total: {articulo.cantidad}, Ya reservado: {total_reservado}"
                    )

        return ReservaRepository.update(db, reserva_id, reserva_data)

    @staticmethod
    def delete_reserva(db: Session, reserva_id: int) -> bool:
        """
        Eliminar una reserva.

        Args:
            db: Sesión de base de datos
            reserva_id: ID de la reserva a eliminar

        Returns:
            True si se eliminó, False si no existe
        """
        return ReservaRepository.delete(db, reserva_id)

    @staticmethod
    def count_reservas(db: Session) -> int:
        """
        Contar el total de reservas.

        Args:
            db: Sesión de base de datos

        Returns:
            Número total de reservas
        """
        return ReservaRepository.count(db)

    @staticmethod
    def check_sala_availability(
        db: Session, sala_id: int, fecha_inicio: datetime, fecha_fin: datetime
    ) -> bool:
        """
        Verificar si una sala está disponible en un horario específico.

        Args:
            db: Sesión de base de datos
            sala_id: ID de la sala
            fecha_inicio: Fecha y hora de inicio
            fecha_fin: Fecha y hora de fin

        Returns:
            True si está disponible, False si hay conflictos
        """
        conflicts = ReservaRepository.check_conflicts(
            db, sala_id, fecha_inicio, fecha_fin
        )
        return len(conflicts) == 0
