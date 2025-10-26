

"""
Servicio proxy para operaciones de Sala.

Este módulo solo reenvía las operaciones al microservicio Java.
No guarda ni consulta datos en la base local.
"""
from typing import Optional
from app.schemas.sala import SalaCreate, SalaUpdate
from app.services.java_client import JavaServiceClient


class SalaService:
    """Servicio para operaciones de negocio de Sala como proxy Java."""

    @staticmethod
    async def create_sala(sala_data: SalaCreate):
        """Crea una sala en el sistema Java usando los datos proporcionados."""
        java_payload = sala_data.model_dump()
        result = await JavaServiceClient.create_sala(java_payload)
        if not result:
            raise ValueError(
                "No se pudo crear la sala en el sistema de gestión de salas (Java). "
                "Intente más tarde."
            )
        return result

    @staticmethod
    async def get_sala_by_id(sala_id: int):
        """Obtiene una sala por su ID desde el sistema Java."""
        result = await JavaServiceClient.get_sala(sala_id)
        return result

    @staticmethod
    async def get_salas() -> list:
        """Obtiene la lista de todas las salas desde el sistema Java."""
        result = await JavaServiceClient.get_salas()
        return result

    @staticmethod
    async def get_salas_by_capacidad(min_capacidad: int, max_capacidad: Optional[int] = None) -> list:
        """Filtra salas por capacidad mínima y máxima."""
        result = await JavaServiceClient.get_salas()
        filtered = [
            s for s in result
            if s.get("capacidad", 0) >= min_capacidad and
            (max_capacidad is None or s.get("capacidad", 0) <= max_capacidad)
        ]
        return filtered

    @staticmethod
    async def update_sala(sala_id: int, sala_data: SalaUpdate):
        """Actualiza los datos de una sala en el sistema Java."""
        java_payload = sala_data.model_dump()
        result = await JavaServiceClient.update_sala(sala_id, java_payload)
        if not result:
            raise ValueError(
                "No se pudo actualizar la sala en el sistema de gestión de salas (Java). "
                "Intente más tarde."
            )
        return result

    @staticmethod
    async def delete_sala(sala_id: int) -> bool:
        """Elimina una sala por su ID en el sistema Java."""
        result = await JavaServiceClient.delete_sala(sala_id)
        if not result:
            raise ValueError(
                "No se pudo eliminar la sala en el sistema de gestión de salas (Java). "
                "Intente más tarde."
            )
        return result

    @staticmethod
    async def count_salas(min_capacidad: Optional[int] = None) -> int:
        """Cuenta la cantidad de salas, opcionalmente filtrando por capacidad mínima."""
        result = await JavaServiceClient.get_salas()
        if min_capacidad is not None:
            result = [s for s in result if s.get("capacidad", 0) >= min_capacidad]
        return len(result)

    @staticmethod
    async def validate_sala_exists(sala_id: int):
        """Valida si una sala existe en el sistema Java."""
        is_java_up = await JavaServiceClient.check_service_health()
        if not is_java_up:
            return {
                "error": (
                    "El sistema de gestión de salas no está disponible en este momento. "
                    "Por favor, intente más tarde."
                )
            }
        exists = await JavaServiceClient.validate_sala_exists(sala_id)
        return exists

    @staticmethod
    async def get_salas_by_min_capacidad(min_capacidad: int) -> list:
        """Obtiene salas con capacidad mayor o igual a la mínima indicada."""
        result = await JavaServiceClient.get_salas()
        filtered = [s for s in result if s.get("capacidad", 0) >= min_capacidad]
        return filtered
