"""
Repositorio para operaciones CRUD de Sala.

Este módulo contiene las operaciones de base de datos para el modelo Sala,
incluyendo crear, leer, actualizar y eliminar registros.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.sala import Sala
from app.schemas.sala import SalaCreate, SalaUpdate


class SalaRepository:
    """Repositorio para operaciones CRUD de Sala."""

    @staticmethod
    def create(db: Session, sala_data: SalaCreate) -> Sala:
        """Crear una nueva sala."""
        db_sala = Sala(
            nombre=sala_data.nombre,
            capacidad=sala_data.capacidad
        )
        db.add(db_sala)
        db.commit()
        db.refresh(db_sala)
        return db_sala

    @staticmethod
    def get_by_id(db: Session, sala_id: int) -> Optional[Sala]:
        """Obtener una sala por su ID."""
        return db.query(Sala).filter(Sala.id == sala_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, min_capacidad: Optional[int] = None) -> List[Sala]:
        """Obtener todas las salas con filtros opcionales."""
        query = db.query(Sala)
        
        if min_capacidad is not None:
            query = query.filter(Sala.capacidad >= min_capacidad)
            
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_by_capacidad(db: Session, min_capacidad: int, max_capacidad: Optional[int] = None, 
                        skip: int = 0, limit: int = 100) -> List[Sala]:
        """Obtener salas por rango de capacidad."""
        query = db.query(Sala).filter(Sala.capacidad >= min_capacidad)
        
        if max_capacidad is not None:
            query = query.filter(Sala.capacidad <= max_capacidad)
            
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, sala_id: int, sala_data: SalaUpdate) -> Optional[Sala]:
        """Actualizar una sala existente."""
        db_sala = db.query(Sala).filter(Sala.id == sala_id).first()
        if not db_sala:
            return None

        update_data = sala_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_sala, field, value)

        db.commit()
        db.refresh(db_sala)
        return db_sala

    @staticmethod
    def delete(db: Session, sala_id: int) -> bool:
        """Eliminar una sala."""
        db_sala = db.query(Sala).filter(Sala.id == sala_id).first()
        if not db_sala:
            return False

        db.delete(db_sala)
        db.commit()
        return True

    @staticmethod
    def count(db: Session, min_capacidad: Optional[int] = None) -> int:
        """Contar salas con filtro opcional."""
        query = db.query(Sala)
        if min_capacidad is not None:
            query = query.filter(Sala.capacidad >= min_capacidad)
        return query.count()