"""
Servicio para operaciones de negocio de Articulo.

Este módulo contiene la lógica de negocio para el modelo Articulo,
incluyendo validaciones y operaciones complejas.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.articulo import Articulo
from app.repositories.articulo_repository import ArticuloRepository
from app.schemas.articulo import ArticuloCreate, ArticuloUpdate


class ArticuloService:
    """Servicio para operaciones de negocio de Articulo."""

    @staticmethod
    def create_articulo(db: Session, articulo_data: ArticuloCreate) -> Articulo:
        """
        Crear un nuevo artículo con validaciones de negocio.

        Args:
            db: Sesión de base de datos
            articulo_data: Datos para crear el artículo

        Returns:
            Artículo creado
        """
        return ArticuloRepository.create(db, articulo_data)

    @staticmethod
    def get_articulo_by_id(db: Session, articulo_id: int) -> Optional[Articulo]:
        """
        Obtener un artículo por su ID.

        Args:
            db: Sesión de base de datos
            articulo_id: ID del artículo

        Returns:
            Artículo encontrado o None
        """
        return ArticuloRepository.get_by_id(db, articulo_id)

    @staticmethod
    def get_articulos(
        db: Session, skip: int = 0, limit: int = 100, disponible: Optional[bool] = None
    ) -> List[Articulo]:
        """
        Obtener lista de artículos con filtros opcionales.

        Args:
            db: Sesión de base de datos
            skip: Registros a omitir (paginación)
            limit: Máximo número de registros
            disponible: Filtro por disponibilidad (opcional)

        Returns:
            Lista de artículos
        """
        return ArticuloRepository.get_all(db, skip, limit, disponible)

    @staticmethod
    def get_articulos_disponibles(
        db: Session, skip: int = 0, limit: int = 100
    ) -> List[Articulo]:
        """
        Obtener solo artículos disponibles.

        Args:
            db: Sesión de base de datos
            skip: Registros a omitir (paginación)
            limit: Máximo número de registros

        Returns:
            Lista de artículos disponibles
        """
        return ArticuloRepository.get_disponibles(db, skip, limit)

    @staticmethod
    def update_articulo(
        db: Session, articulo_id: int, articulo_data: ArticuloUpdate
    ) -> Optional[Articulo]:
        """
        Actualizar un artículo existente.

        Args:
            db: Sesión de base de datos
            articulo_id: ID del artículo a actualizar
            articulo_data: Nuevos datos del artículo

        Returns:
            Artículo actualizado o None si no existe
        """
        return ArticuloRepository.update(db, articulo_id, articulo_data)

    @staticmethod
    def toggle_disponibilidad(db: Session, articulo_id: int) -> Optional[Articulo]:
        """
        Cambiar la disponibilidad de un artículo.

        Args:
            db: Sesión de base de datos
            articulo_id: ID del artículo

        Returns:
            Artículo actualizado o None si no existe
        """
        articulo = ArticuloRepository.get_by_id(db, articulo_id)
        if not articulo:
            return None

        return ArticuloRepository.toggle_disponibilidad(db, articulo_id)

    @staticmethod
    def delete_articulo(db: Session, articulo_id: int) -> bool:
        """
        Eliminar un artículo si no tiene reservas activas.

        Args:
            db: Sesión de base de datos
            articulo_id: ID del artículo a eliminar

        Returns:
            True si se eliminó, False si no existe

        Raises:
            ValueError: Si el artículo tiene reservas activas
        """
        articulo = ArticuloRepository.get_by_id(db, articulo_id)
        if not articulo:
            return False

        # Verificar si tiene reservas (se puede expandir con lógica más compleja)
        if hasattr(articulo, "reservas") and articulo.reservas:
            raise ValueError("No se puede eliminar un artículo con reservas activas")

        return ArticuloRepository.delete(db, articulo_id)

    @staticmethod
    def count_articulos(db: Session, disponible: Optional[bool] = None) -> int:
        """
        Contar artículos con filtro opcional.

        Args:
            db: Sesión de base de datos
            disponible: Filtro por disponibilidad (opcional)

        Returns:
            Número de artículos
        """
        return ArticuloRepository.count(db, disponible)

    @staticmethod
    def validate_articulo_exists(db: Session, articulo_id: int) -> bool:
        """
        Validar que un artículo existe.

        Args:
            db: Sesión de base de datos
            articulo_id: ID del artículo

        Returns:
            True si existe, False si no
        """
        articulo = ArticuloRepository.get_by_id(db, articulo_id)
        return articulo is not None

    @staticmethod
    def validate_articulo_disponible(db: Session, articulo_id: int) -> bool:
        """
        Validar que un artículo existe y está disponible.

        Args:
            db: Sesión de base de datos
            articulo_id: ID del artículo

        Returns:
            True si existe y está disponible, False si no
        """
        articulo = ArticuloRepository.get_by_id(db, articulo_id)
        return articulo is not None and getattr(articulo, "disponible", False)
