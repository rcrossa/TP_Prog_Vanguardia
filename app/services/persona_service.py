"""
Servicio para operaciones de negocio de Persona.

Este módulo contiene la lógica de negocio para el modelo Persona,
incluyendo validaciones y operaciones complejas.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.persona import Persona
from app.schemas.persona import PersonaCreate, PersonaUpdate
from app.repositories.persona_repository import PersonaRepository


class PersonaService:
    """Servicio para operaciones de negocio de Persona."""

    @staticmethod
    def create_persona(db: Session, persona_data: PersonaCreate) -> Persona:
        """
        Crear una nueva persona con validaciones de negocio.
        
        Args:
            db: Sesión de base de datos
            persona_data: Datos para crear la persona
            
        Returns:
            Persona creada
            
        Raises:
            ValueError: Si el email ya existe o es inválido
        """
        # Verificar si el email ya existe
        existing_persona = PersonaRepository.get_by_email(db, persona_data.email)
        if existing_persona:
            raise ValueError(f"Ya existe una persona con el email {persona_data.email}")
            
        return PersonaRepository.create(db, persona_data)

    @staticmethod
    def get_persona_by_id(db: Session, persona_id: int) -> Optional[Persona]:
        """
        Obtener una persona por su ID.
        
        Args:
            db: Sesión de base de datos
            persona_id: ID de la persona
            
        Returns:
            Persona encontrada o None
        """
        return PersonaRepository.get_by_id(db, persona_id)

    @staticmethod
    def get_persona_by_email(db: Session, email: str) -> Optional[Persona]:
        """
        Obtener una persona por su email.
        
        Args:
            db: Sesión de base de datos
            email: Email de la persona
            
        Returns:
            Persona encontrada o None
        """
        return PersonaRepository.get_by_email(db, email)

    @staticmethod
    def get_personas(db: Session, skip: int = 0, limit: int = 100, 
                    nombre: Optional[str] = None) -> List[Persona]:
        """
        Obtener lista de personas con filtros opcionales.
        
        Args:
            db: Sesión de base de datos
            skip: Registros a omitir (paginación)
            limit: Máximo número de registros
            nombre: Filtro por nombre (opcional)
            
        Returns:
            Lista de personas
        """
        return PersonaRepository.get_all(db, skip, limit)

    @staticmethod
    def update_persona(db: Session, persona_id: int, persona_data: PersonaUpdate) -> Optional[Persona]:
        """
        Actualizar una persona existente con validaciones.
        
        Args:
            db: Sesión de base de datos
            persona_id: ID de la persona a actualizar
            persona_data: Nuevos datos de la persona
            
        Returns:
            Persona actualizada o None si no existe
            
        Raises:
            ValueError: Si el nuevo email ya está en uso por otra persona
        """
        # Si se está cambiando el email, verificar que no exista
        if persona_data.email:
            existing_persona = PersonaRepository.get_by_email(db, persona_data.email)
            if existing_persona is not None:
                existing_id = getattr(existing_persona, 'id', None)
                if existing_id and existing_id != persona_id:
                    raise ValueError(f"Ya existe otra persona con el email {persona_data.email}")
        
        return PersonaRepository.update(db, persona_id, persona_data)

    @staticmethod
    def delete_persona(db: Session, persona_id: int) -> bool:
        """
        Eliminar una persona si no tiene reservas activas.
        
        Args:
            db: Sesión de base de datos
            persona_id: ID de la persona a eliminar
            
        Returns:
            True si se eliminó, False si no existe
            
        Raises:
            ValueError: Si la persona tiene reservas activas
        """
        persona = PersonaRepository.get_by_id(db, persona_id)
        if not persona:
            return False
            
        # Verificar si tiene reservas (se puede expandir con lógica más compleja)
        if hasattr(persona, 'reservas') and persona.reservas:
            raise ValueError("No se puede eliminar una persona con reservas activas")
        
        return PersonaRepository.delete(db, persona_id)

    @staticmethod
    def count_personas(db: Session) -> int:
        """
        Contar el total de personas registradas.
        
        Args:
            db: Sesión de base de datos
            
        Returns:
            Número total de personas
        """
        return PersonaRepository.count(db)

    @staticmethod
    def validate_persona_exists(db: Session, persona_id: int) -> bool:
        """
        Validar que una persona existe.
        
        Args:
            db: Sesión de base de datos
            persona_id: ID de la persona
            
        Returns:
            True si existe, False si no
        """
        persona = PersonaRepository.get_by_id(db, persona_id)
        return persona is not None