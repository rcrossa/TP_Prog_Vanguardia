"""
Repositorio para operaciones CRUD de Reserva.

Este módulo contiene las operaciones de base de datos para el modelo Reserva,
incluyendo crear, leer, actualizar y eliminar registros con relaciones.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.reserva import Reserva
from app.schemas.reserva import ReservaCreate, ReservaUpdate


class ReservaRepository:
    """Repositorio para operaciones CRUD de Reserva."""

    @staticmethod
    def create(db: Session, reserva_data: ReservaCreate) -> Reserva:
        """Crear una nueva reserva."""
        db_reserva = Reserva(
            id_persona=reserva_data.id_persona,
            id_sala=reserva_data.id_sala,
            id_articulo=reserva_data.id_articulo,
            fecha_hora_inicio=reserva_data.fecha_hora_inicio,
            fecha_hora_fin=reserva_data.fecha_hora_fin
        )
        db.add(db_reserva)
        db.commit()
        db.refresh(db_reserva)
        return db_reserva

    @staticmethod
    def get_by_id(db: Session, reserva_id: int) -> Optional[Reserva]:
        """Obtener una reserva por su ID con relaciones cargadas."""
        return db.query(Reserva).options(
            joinedload(Reserva.persona),
            joinedload(Reserva.sala),
            joinedload(Reserva.articulo)
        ).filter(Reserva.id == reserva_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Reserva]:
        """Obtener todas las reservas con relaciones cargadas."""
        return db.query(Reserva).options(
            joinedload(Reserva.persona),
            joinedload(Reserva.sala),
            joinedload(Reserva.articulo)
        ).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_persona(db: Session, persona_id: int, skip: int = 0, limit: int = 100) -> List[Reserva]:
        """Obtener reservas por persona."""
        return db.query(Reserva).options(
            joinedload(Reserva.persona),
            joinedload(Reserva.sala),
            joinedload(Reserva.articulo)
        ).filter(Reserva.id_persona == persona_id).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_sala(db: Session, sala_id: int, skip: int = 0, limit: int = 100) -> List[Reserva]:
        """Obtener reservas por sala."""
        return db.query(Reserva).options(
            joinedload(Reserva.persona),
            joinedload(Reserva.sala),
            joinedload(Reserva.articulo)
        ).filter(Reserva.id_sala == sala_id).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_articulo(db: Session, articulo_id: int, skip: int = 0, limit: int = 100) -> List[Reserva]:
        """Obtener reservas por artículo."""
        return db.query(Reserva).options(
            joinedload(Reserva.persona),
            joinedload(Reserva.sala),
            joinedload(Reserva.articulo)
        ).filter(Reserva.id_articulo == articulo_id).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_fecha_range(db: Session, fecha_inicio: datetime, fecha_fin: Optional[datetime] = None, 
                          skip: int = 0, limit: int = 100) -> List[Reserva]:
        """Obtener reservas por rango de fechas."""
        query = db.query(Reserva).options(
            joinedload(Reserva.persona),
            joinedload(Reserva.sala),
            joinedload(Reserva.articulo)
        ).filter(Reserva.fecha_hora_inicio >= fecha_inicio)
        
        if fecha_fin:
            query = query.filter(Reserva.fecha_hora_fin <= fecha_fin)
            
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def check_conflicts(db: Session, sala_id: int, fecha_inicio: datetime, 
                       fecha_fin: datetime, exclude_reserva_id: Optional[int] = None) -> List[Reserva]:
        """Verificar conflictos de reservas en una sala."""
        query = db.query(Reserva).filter(
            Reserva.id_sala == sala_id,
            Reserva.fecha_hora_inicio < fecha_fin,
            Reserva.fecha_hora_fin > fecha_inicio
        )
        
        if exclude_reserva_id:
            query = query.filter(Reserva.id != exclude_reserva_id)
            
        return query.all()

    @staticmethod
    def update(db: Session, reserva_id: int, reserva_data: ReservaUpdate) -> Optional[Reserva]:
        """Actualizar una reserva existente."""
        db_reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
        if not db_reserva:
            return None

        update_data = reserva_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_reserva, field, value)

        db.commit()
        db.refresh(db_reserva)
        return db_reserva

    @staticmethod
    def delete(db: Session, reserva_id: int) -> bool:
        """Eliminar una reserva."""
        db_reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
        if not db_reserva:
            return False

        db.delete(db_reserva)
        db.commit()
        return True

    @staticmethod
    def count(db: Session) -> int:
        """Contar total de reservas."""
        return db.query(Reserva).count()