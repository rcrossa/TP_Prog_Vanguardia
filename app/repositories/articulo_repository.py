
"""
Repositorio para operaciones CRUD de Articulo.

Este módulo contiene las operaciones de base de datos para el modelo Articulo,
incluyendo crear, leer, actualizar y eliminar registros.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.articulo import Articulo
from app.schemas.articulo import ArticuloCreate, ArticuloUpdate


class ArticuloRepository:
    """Repositorio para operaciones CRUD de Articulo."""

    @staticmethod
    def create(db: Session, articulo_data: ArticuloCreate) -> Articulo:
        """Crear un nuevo artículo."""
        db_articulo = Articulo(
            nombre=articulo_data.nombre,
            descripcion=articulo_data.descripcion,
            cantidad=articulo_data.cantidad,
            categoria=articulo_data.categoria,
            disponible=articulo_data.disponible,
        )
        db.add(db_articulo)
        db.commit()
        db.refresh(db_articulo)
        return db_articulo

    @staticmethod
    def get_by_id(db: Session, articulo_id: int) -> Optional[Articulo]:
        """Obtener un artículo por su ID."""
        return db.query(Articulo).filter(Articulo.id == articulo_id).first()

    @staticmethod
    def get_all(
        db: Session, skip: int = 0, limit: int = 100, disponible: Optional[bool] = None
    ) -> List[Articulo]:
        """Obtener todos los artículos con filtros opcionales."""
        query = db.query(Articulo)

        if disponible is not None:
            query = query.filter(Articulo.disponible == disponible)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_disponibles(db: Session, skip: int = 0, limit: int = 100) -> List[Articulo]:
        """Obtener solo artículos disponibles."""
        return (
            db.query(Articulo)
            .filter(Articulo.disponible.is_(True))
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update(
        db: Session, articulo_id: int, articulo_data: ArticuloUpdate
    ) -> Optional[Articulo]:
        """Actualizar un artículo existente."""
        db_articulo = db.query(Articulo).filter(Articulo.id == articulo_id).first()
        if not db_articulo:
            return None

        update_data = articulo_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_articulo, field, value)

        db.commit()
        db.refresh(db_articulo)
        return db_articulo

    @staticmethod
    def delete(db: Session, articulo_id: int) -> bool:
        """Eliminar un artículo."""
        db_articulo = db.query(Articulo).filter(Articulo.id == articulo_id).first()
        if not db_articulo:
            return False

        db.delete(db_articulo)
        db.commit()
        return True

    @staticmethod
    def set_disponibilidad(
        db: Session, articulo_id: int, disponible: bool
    ) -> Optional[Articulo]:
        """Cambiar la disponibilidad de un artículo."""
        db_articulo = db.query(Articulo).filter(Articulo.id == articulo_id).first()
        if not db_articulo:
            return None

        db_articulo.disponible = disponible
        db.commit()
        db.refresh(db_articulo)
        return db_articulo

    @staticmethod
    def toggle_disponibilidad(db: Session, articulo_id: int) -> Optional[Articulo]:
        """Cambiar la disponibilidad de un artículo."""
        db_articulo = db.query(Articulo).filter(Articulo.id == articulo_id).first()
        if not db_articulo:
            return None

        # Cambiar el estado de disponibilidad
        current_disponible = getattr(db_articulo, "disponible", False)
        db_articulo.disponible = not current_disponible
        db.commit()
        db.refresh(db_articulo)
        return db_articulo

    @staticmethod
    def count(db: Session, disponible: Optional[bool] = None) -> int:
        """Contar artículos con filtro opcional."""
        query = db.query(Articulo)
        if disponible is not None:
            query = query.filter(Articulo.disponible == disponible)
        return query.count()
