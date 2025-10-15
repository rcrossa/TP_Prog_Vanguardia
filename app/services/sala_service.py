"""
Servicio para operaciones de negocio de Sala.

Este módulo contiene la lógica de negocio para el modelo Sala,
incluyendo validaciones y operaciones complejas.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.sala import Sala
from app.schemas.sala import SalaCreate, SalaUpdate
from app.repositories.sala_repository import SalaRepository


class SalaService:
    """Servicio para operaciones de negocio de Sala."""

    @staticmethod
    def create_sala(db: Session, sala_data: SalaCreate) -> Sala:
        """
        Crear una nueva sala con validaciones de negocio.
        
        Args:
            db: Sesión de base de datos
            sala_data: Datos para crear la sala
            
        Returns:
            Sala creada
            
        Raises:
            ValueError: Si los datos son inválidos
        """
        # Validar capacidad mínima
        if sala_data.capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor a 0")
            
        return SalaRepository.create(db, sala_data)

    @staticmethod
    def get_sala_by_id(db: Session, sala_id: int) -> Optional[Sala]:
        """
        Obtener una sala por su ID.
        
        Args:
            db: Sesión de base de datos
            sala_id: ID de la sala
            
        Returns:
            Sala encontrada o None
        """
        return SalaRepository.get_by_id(db, sala_id)

    @staticmethod
    def get_salas(db: Session, skip: int = 0, limit: int = 100, 
                  min_capacidad: Optional[int] = None) -> List[Sala]:
        """
        Obtener lista de salas con filtros opcionales.
        
        Args:
            db: Sesión de base de datos
            skip: Registros a omitir (paginación)
            limit: Máximo número de registros
            min_capacidad: Capacidad mínima requerida (opcional)
            
        Returns:
            Lista de salas
        """
        return SalaRepository.get_all(db, skip, limit, min_capacidad)

    @staticmethod
    def get_salas_by_capacidad(db: Session, min_capacidad: int, 
                              max_capacidad: Optional[int] = None,
                              skip: int = 0, limit: int = 100) -> List[Sala]:
        """
        Obtener salas por rango de capacidad.
        
        Args:
            db: Sesión de base de datos
            min_capacidad: Capacidad mínima
            max_capacidad: Capacidad máxima (opcional)
            skip: Registros a omitir (paginación)
            limit: Máximo número de registros
            
        Returns:
            Lista de salas en el rango de capacidad
        """
        return SalaRepository.get_by_capacidad(db, min_capacidad, max_capacidad, skip, limit)

    @staticmethod
    def update_sala(db: Session, sala_id: int, sala_data: SalaUpdate) -> Optional[Sala]:
        """
        Actualizar una sala existente con validaciones.
        
        Args:
            db: Sesión de base de datos
            sala_id: ID de la sala a actualizar
            sala_data: Nuevos datos de la sala
            
        Returns:
            Sala actualizada o None si no existe
            
        Raises:
            ValueError: Si la nueva capacidad es inválida
        """
        # Validar capacidad si se está actualizando
        if sala_data.capacidad is not None and sala_data.capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor a 0")
            
        return SalaRepository.update(db, sala_id, sala_data)

    @staticmethod
    def delete_sala(db: Session, sala_id: int) -> bool:
        """
        Eliminar una sala si no tiene reservas activas.
        
        Args:
            db: Sesión de base de datos
            sala_id: ID de la sala a eliminar
            
        Returns:
            True si se eliminó, False si no existe
            
        Raises:
            ValueError: Si la sala tiene reservas activas
        """
        sala = SalaRepository.get_by_id(db, sala_id)
        if not sala:
            return False
            
        # Verificar si tiene reservas (se puede expandir con lógica más compleja)
        if hasattr(sala, 'reservas') and sala.reservas:
            raise ValueError("No se puede eliminar una sala con reservas activas")
        
        return SalaRepository.delete(db, sala_id)

    @staticmethod
    def count_salas(db: Session, min_capacidad: Optional[int] = None) -> int:
        """
        Contar salas con filtro opcional.
        
        Args:
            db: Sesión de base de datos
            min_capacidad: Capacidad mínima (opcional)
            
        Returns:
            Número de salas
        """
        return SalaRepository.count(db, min_capacidad)

    @staticmethod
    def validate_sala_exists(db: Session, sala_id: int) -> bool:
        """
        Validar que una sala existe.
        
        Args:
            db: Sesión de base de datos
            sala_id: ID de la sala
            
        Returns:
            True si existe, False si no
        """
        sala = SalaRepository.get_by_id(db, sala_id)
        return sala is not None

    @staticmethod
    def get_salas_by_min_capacidad(db: Session, min_capacidad: int) -> List[Sala]:
        """
        Obtener todas las salas que pueden acomodar una capacidad mínima.
        
        Args:
            db: Sesión de base de datos
            min_capacidad: Capacidad mínima requerida
            
        Returns:
            Lista de salas aptas
        """
        return SalaRepository.get_by_capacidad(db, min_capacidad)