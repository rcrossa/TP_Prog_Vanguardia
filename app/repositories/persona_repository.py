"""
Repositorio para operaciones CRUD de Persona.

Este módulo contiene las operaciones de base de datos para el modelo Persona,
incluyendo crear, leer, actualizar y eliminar registros.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.persona import Persona
from app.schemas.persona import PersonaCreate, PersonaUpdate


class PersonaRepository:
    """Repositorio para operaciones CRUD de Persona."""

    @staticmethod
    def create(db: Session, persona_data: PersonaCreate) -> Persona:
        """Crear una nueva persona."""
        db_persona = Persona(
            nombre=persona_data.nombre,
            email=persona_data.email
        )
        db.add(db_persona)
        db.commit()
        db.refresh(db_persona)
        return db_persona

    @staticmethod
    def get_by_id(db: Session, persona_id: int) -> Optional[Persona]:
        """Obtener una persona por su ID."""
        return db.query(Persona).filter(Persona.id == persona_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[Persona]:
        """Obtener una persona por su email."""
        return db.query(Persona).filter(Persona.email == email).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Persona]:
        """Obtener todas las personas con paginación."""
        return db.query(Persona).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, persona_id: int, persona_data: PersonaUpdate) -> Optional[Persona]:
        """Actualizar una persona existente."""
        db_persona = db.query(Persona).filter(Persona.id == persona_id).first()
        if not db_persona:
            return None

        update_data = persona_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_persona, field, value)

        db.commit()
        db.refresh(db_persona)
        return db_persona

    @staticmethod
    def delete(db: Session, persona_id: int) -> bool:
        """Eliminar una persona."""
        db_persona = db.query(Persona).filter(Persona.id == persona_id).first()
        if not db_persona:
            return False

        db.delete(db_persona)
        db.commit()
        return True

    @staticmethod
    def count(db: Session) -> int:
        """Contar el total de personas."""
        return db.query(Persona).count()