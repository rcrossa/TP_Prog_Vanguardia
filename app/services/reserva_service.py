"""
Servicio para operaciones de negocio de Reserva.

Este módulo contiene la lógica de negocio para el modelo Reserva,
incluyendo validaciones complejas y operaciones de reservas.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.reserva import Reserva
from app.schemas.reserva import ReservaCreate, ReservaUpdate
from app.repositories.reserva_repository import ReservaRepository
from app.services.persona_service import PersonaService
from app.services.articulo_service import ArticuloService
from app.services.sala_service import SalaService


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
            raise ValueError(f"No existe una persona con ID {reserva_data.id_persona}")

        # Validar fechas
        if reserva_data.fecha_hora_fin <= reserva_data.fecha_hora_inicio:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")

        # Validar que no se está reservando en el pasado
        if reserva_data.fecha_hora_inicio < datetime.now():
            raise ValueError("No se pueden crear reservas en el pasado")

        # Una reserva debe ser para un artículo O una sala, no ambos ni ninguno
        has_articulo = reserva_data.id_articulo is not None
        has_sala = reserva_data.id_sala is not None
        
        if not has_articulo and not has_sala:
            raise ValueError("La reserva debe ser para un artículo o una sala")
        
        if has_articulo and has_sala:
            raise ValueError("La reserva no puede ser para un artículo y una sala al mismo tiempo")

        # Validaciones específicas según el tipo de reserva
        if has_articulo:
            ReservaService._validate_articulo_reservation(db, reserva_data)
        
        if has_sala:
            ReservaService._validate_sala_reservation(db, reserva_data)

        return ReservaRepository.create(db, reserva_data)

    @staticmethod
    def _validate_articulo_reservation(db: Session, reserva_data: ReservaCreate) -> None:
        """Validar reserva de artículo."""
        # Verificar que el artículo existe y está disponible
        if reserva_data.id_articulo is not None:
            if not ArticuloService.validate_articulo_disponible(db, reserva_data.id_articulo):
                raise ValueError(f"El artículo con ID {reserva_data.id_articulo} no existe o no está disponible")

    @staticmethod
    def _validate_sala_reservation(db: Session, reserva_data: ReservaCreate) -> None:
        """Validar reserva de sala."""
        # Verificar que la sala existe
        if reserva_data.id_sala is not None:
            if not SalaService.validate_sala_exists(db, reserva_data.id_sala):
                raise ValueError(f"No existe una sala con ID {reserva_data.id_sala}")

            # Verificar conflictos de horario en la sala
            conflicts = ReservaRepository.check_conflicts(
                db, 
                reserva_data.id_sala,
                reserva_data.fecha_hora_inicio,
                reserva_data.fecha_hora_fin
            )
            
            if conflicts:
                raise ValueError(f"Ya existe una reserva en la sala para el horario especificado")

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
    def get_reservas_by_persona(db: Session, persona_id: int, 
                               skip: int = 0, limit: int = 100) -> List[Reserva]:
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
    def get_reservas_by_sala(db: Session, sala_id: int, 
                            skip: int = 0, limit: int = 100) -> List[Reserva]:
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
    def get_reservas_by_articulo(db: Session, articulo_id: int,
                                skip: int = 0, limit: int = 100) -> List[Reserva]:
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
    def get_reservas_by_fecha_range(db: Session, fecha_inicio: datetime,
                                   fecha_fin: Optional[datetime] = None,
                                   skip: int = 0, limit: int = 100) -> List[Reserva]:
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
        return ReservaRepository.get_by_fecha_range(db, fecha_inicio, fecha_fin, skip, limit)

    @staticmethod
    def update_reserva(db: Session, reserva_id: int, reserva_data: ReservaUpdate) -> Optional[Reserva]:
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
        if reserva_data.fecha_hora_inicio and reserva_data.fecha_hora_fin:
            if reserva_data.fecha_hora_fin <= reserva_data.fecha_hora_inicio:
                raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")

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
    def check_sala_availability(db: Session, sala_id: int, 
                               fecha_inicio: datetime, fecha_fin: datetime) -> bool:
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
        conflicts = ReservaRepository.check_conflicts(db, sala_id, fecha_inicio, fecha_fin)
        return len(conflicts) == 0