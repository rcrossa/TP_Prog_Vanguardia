
"""
Cliente HTTP para comunicación con el servicio Java.

Este módulo maneja todas las llamadas HTTP al microservicio Java
que gestiona Salas y Artículos.
"""
import logging
from typing import Optional, Dict, Any
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)

class JavaServiceClient:
    """Cliente para interactuar con el microservicio Java que gestiona Salas y Artículos."""
    @staticmethod
    async def validate_articulo_exists(articulo_id: int) -> bool:
        """
        Verificar si un artículo existe en el servicio Java.

        Args:
            articulo_id: ID del artículo a verificar

        Returns:
            True si el artículo existe, False en caso contrario
        """
        try:
            async with httpx.AsyncClient(timeout=JavaServiceClient.TIMEOUT) as client:
                response = await client.get(
                    f"{JavaServiceClient.JAVA_SERVICE_URL}/api/articulos/{articulo_id}"
                )
                if response.status_code == 200:
                    logger.info("✅ Artículo %s validado exitosamente.", articulo_id)
                    return True
                elif response.status_code == 404:
                    logger.warning("⚠️ Artículo %s no encontrado en Java Service", articulo_id)
                    return False
                else:
                    logger.error("❌ Error al validar artículo %s: Status %s",
                                 articulo_id, response.status_code)
                    return False
        except httpx.TimeoutException:
            logger.error("⏱️ Timeout al conectar con Java Service para artículo %s", articulo_id)
            return False
        except httpx.ConnectError:
            logger.error("🔌 No se pudo conectar con Java Service para artículo %s", articulo_id)
            return False
        except httpx.RequestError as e:
            logger.error("❌ Error al validar artículo %s en Java: %s", articulo_id, e)
            return False
    # """
    # Cliente para interactuar con el microservicio Java que gestiona Salas y Artículos.
    # Proporciona métodos asíncronos para operaciones CRUD y validaciones.
    # """
    TIMEOUT = 5.0
    JAVA_SERVICE_URL = getattr(settings, "JAVA_SERVICE_URL", "http://localhost:8080")

    # Métodos de Artículos
    @staticmethod
    async def get_articulos() -> list:
        """
        Obtener lista de artículos desde el microservicio Java.
        Returns:
            list: Lista de artículos (dicts) o lista vacía si falla
        """
        try:
            async with httpx.AsyncClient(timeout=JavaServiceClient.TIMEOUT) as client:
                response = await client.get(f"{JavaServiceClient.JAVA_SERVICE_URL}/api/articulos")
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(
                        "❌ Error al obtener artículos de Java: Status %s", response.status_code)
                    return []
        except httpx.RequestError as e:
            logger.error("❌ Error al obtener artículos de Java: %s", e)
            return []

    @staticmethod
    async def get_articulo(articulo_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtener un artículo por ID desde el microservicio Java.
        Args:
            articulo_id (int): ID del artículo
        Returns:
            Optional[Dict[str, Any]]: Diccionario con el artículo o None si no existe
        """
        try:
            async with httpx.AsyncClient(timeout=JavaServiceClient.TIMEOUT) as client:
                response = await client.get(
                    f"{JavaServiceClient.JAVA_SERVICE_URL}/api/articulos/{articulo_id}")
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    return None
                else:
                    logger.error(
                        "❌ Error al obtener artículo de Java: Status %s", response.status_code)
                    return None
        except httpx.RequestError as e:
            logger.error("❌ Error al obtener artículo de Java: %s", e)
            return None

    @staticmethod
    async def create_articulo(articulo_data: dict) -> Optional[Dict[str, Any]]:
        """
        Crear un artículo en el microservicio Java.
        Args:
            articulo_data (dict): Diccionario con los datos del artículo
        Returns:
            Optional[Dict[str, Any]]: Diccionario con el artículo creado o None si falla
        """
        try:
            async with httpx.AsyncClient(timeout=JavaServiceClient.TIMEOUT) as client:
                response = await client.post(
                    f"{JavaServiceClient.JAVA_SERVICE_URL}/api/articulos",
                    json=articulo_data
                )
                if response.status_code == 201:
                    return response.json()
                else:
                    logger.error(
                        "❌ Error al crear artículo en Java: Status %s", response.status_code)
                    return None
        except httpx.RequestError as e:
            logger.error("❌ Error al crear artículo en Java: %s", e)
            return None

    @staticmethod
    async def update_articulo(articulo_id: int, articulo_data: dict) -> Optional[Dict[str, Any]]:
        """
        Actualizar un artículo en el microservicio Java.
        Args:
            articulo_id (int): ID del artículo a actualizar
            articulo_data (dict): Diccionario con los datos a actualizar
        Returns:
            Optional[Dict[str, Any]]: Diccionario con el artículo actualizado o None si falla
        """
        try:
            async with httpx.AsyncClient(timeout=JavaServiceClient.TIMEOUT) as client:
                response = await client.put(
                    f"{JavaServiceClient.JAVA_SERVICE_URL}/api/articulos/{articulo_id}",
                    json=articulo_data
                )
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(
                        "❌ Error al actualizar artículo en Java: Status %s", response.status_code)
                    return None
        except httpx.RequestError as e:
            logger.error("❌ Error al actualizar artículo en Java: %s", e)
            return None

    @staticmethod
    async def delete_articulo(articulo_id: int) -> bool:
        """
        Eliminar un artículo en el microservicio Java.
        Args:
            articulo_id (int): ID del artículo a eliminar
        Returns:
            bool: True si se eliminó correctamente, False si no existe o falla
        """
        try:
            async with httpx.AsyncClient(timeout=JavaServiceClient.TIMEOUT) as client:
                response = await client.delete(
                    f"{JavaServiceClient.JAVA_SERVICE_URL}/api/articulos/{articulo_id}"
                )
                if response.status_code == 204:
                    logger.info("✅ Artículo %s eliminado en Java Service", articulo_id)
                    return True
                elif response.status_code == 404:
                    logger.warning(
                        "⚠️ Artículo %s no encontrado en Java Service para eliminar", articulo_id)
                    return False
                else:
                    logger.error(
                        "❌ Error al eliminar artículo %s en Java: Status %s", 
                         articulo_id, response.status_code)
                    return False
        except httpx.RequestError as e:
            logger.error("❌ Error al eliminar artículo en Java: %s", e)
            return False

    @staticmethod
    async def get_articulo_details(articulo_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtener detalles completos de un artículo desde el servicio Java.
        Args:
            articulo_id (int): ID del artículo
        Returns:
            Optional[Dict[str, Any]]: Diccionario con datos del artículo o None si no existe
        """
        try:
            async with httpx.AsyncClient(timeout=JavaServiceClient.TIMEOUT) as client:
                response = await client.get(
                    f"{JavaServiceClient.JAVA_SERVICE_URL}/api/articulos/{articulo_id}"
                )
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.warning("⚠️ No se pudieron obtener detalles de artículo %s", articulo_id)
                    return None
        except httpx.RequestError as e:
            logger.error("❌ Error al obtener detalles de artículo %s: %s", articulo_id, e)
            return None

    # Métodos de Salas
    @staticmethod
    async def get_salas() -> list:
        """
        Obtener lista de salas desde el microservicio Java.
        Returns:
            list: Lista de salas (dicts) o lista vacía si falla
        """
        try:
            async with httpx.AsyncClient(timeout=JavaServiceClient.TIMEOUT) as client:
                response = await client.get(f"{JavaServiceClient.JAVA_SERVICE_URL}/api/salas")
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(
                        "❌ Error al obtener salas de Java: Status %s", response.status_code)
                    return []
        except httpx.RequestError as e:
            logger.error("❌ Error al obtener salas de Java: %s", e)
            return []

    @staticmethod
    async def get_sala(sala_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtener una sala por ID desde el microservicio Java.
        Args:
            sala_id: ID de la sala
        Returns:
            Optional[Dict[str, Any]]: Diccionario con la sala o None si no existe
        """
        try:
            async with httpx.AsyncClient(timeout=JavaServiceClient.TIMEOUT) as client:
                response = await client.get(
                    f"{JavaServiceClient.JAVA_SERVICE_URL}/api/salas/{sala_id}"
                )
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    return None
                else:
                    logger.error("❌ Error al obtener sala de Java: Status %s", response.status_code)
                    return None
        except httpx.RequestError as e:
            logger.error("❌ Error al obtener sala de Java: %s", e)
            return None

    @staticmethod
    async def create_sala(sala_data: dict) -> Optional[Dict[str, Any]]:
        """
        Crear una sala en el microservicio Java.
        Args:
            sala_data (dict): Diccionario con los datos de la sala
        Returns:
            Optional[Dict[str, Any]]: Diccionario con la sala creada o None si falla
        """
        try:
            async with httpx.AsyncClient(timeout=JavaServiceClient.TIMEOUT) as client:
                response = await client.post(
                    f"{JavaServiceClient.JAVA_SERVICE_URL}/api/salas",
                    json=sala_data
                )
                if response.status_code == 201:
                    return response.json()
                else:
                    logger.error("❌ Error al crear sala en Java: Status %s", response.status_code)
                    return None
        except httpx.RequestError as e:
            logger.error("❌ Error al crear sala en Java: %s", e)
            return None

    @staticmethod
    async def update_sala(sala_id: int, sala_data: dict) -> Optional[Dict[str, Any]]:
        """
        Actualizar una sala en el microservicio Java.
        Args:
            sala_id: ID de la sala a actualizar
            sala_data: Diccionario con los datos a actualizar
        Returns:
            Optional[Dict[str, Any]]: Diccionario con la sala actualizada o None si falla
        """
        try:
            async with httpx.AsyncClient(timeout=JavaServiceClient.TIMEOUT) as client:
                response = await client.put(
                    f"{JavaServiceClient.JAVA_SERVICE_URL}/api/salas/{sala_id}",
                    json=sala_data
                )
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(
                        "❌ Error al actualizar sala en Java: Status %s", response.status_code)
                    return None
        except httpx.RequestError as e:
            logger.error("❌ Error al actualizar sala en Java: %s", e)
            return None

    @staticmethod
    async def delete_sala(sala_id: int) -> bool:
        """
        Eliminar una sala en el microservicio Java.

        Args:
            sala_id: ID de la sala a eliminar

        Returns:
            True si se eliminó correctamente, False si no existe o falla
        """
        try:
            async with httpx.AsyncClient(
                timeout=JavaServiceClient.TIMEOUT) as client:
                response = await client.delete(
                    f"{JavaServiceClient.JAVA_SERVICE_URL}/api/salas/{sala_id}"
                )
                if response.status_code == 204:
                    logger.info("✅ Sala %s eliminada en Java Service", sala_id)
                    return True
                elif response.status_code == 404:
                    logger.warning(
                        "⚠️ Sala %s no encontrada en Java Service para eliminar", sala_id)
                    return False
                else:
                    logger.error(
                        "❌ Error al eliminar sala %s en Java: Status %s",
                          sala_id, response.status_code)
                    return False
        except httpx.RequestError as e:
            logger.error("❌ Error al eliminar sala %s en Java: %s", sala_id, e)
            return False

    @staticmethod
    async def validate_sala_exists(sala_id: int) -> bool:
        """
        Verificar si una sala existe en el servicio Java.

        Args:
            sala_id: ID de la sala a verificar

        Returns:
            True si la sala existe, False en caso contrario
        """
        try:
            async with httpx.AsyncClient(timeout=JavaServiceClient.TIMEOUT) as client:
                response = await client.get(
                    f"{JavaServiceClient.JAVA_SERVICE_URL}/api/salas/{sala_id}"
                )

                if response.status_code == 200:
                    logger.info("✅ Sala %s validada exitosamente desde Java Service", sala_id)
                    return True
                elif response.status_code == 404:
                    logger.warning("⚠️ Sala %s no encontrada en Java Service", sala_id)
                    return False
                else:
                    logger.error("❌ Error al validar sala %s: Status %s",
                                  sala_id, response.status_code)
                    return False

        except httpx.TimeoutException:
            logger.error("⏱️ Timeout al conectar con Java Service para sala %s", sala_id)
            # Si el servicio Java no está disponible, fallback a validación local
            return False
        except httpx.ConnectError:
            logger.error("🔌 No se pudo conectar con Java Service para sala %s", sala_id)
            # Si el servicio Java no está disponible, fallback a validación local
            return False
        except httpx.RequestError as e:
            logger.error("❌ Error inesperado al validar sala %s: %s", sala_id, str(e))
            return False

    @staticmethod
    async def get_sala_details(sala_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtener detalles completos de una sala desde el servicio Java.

        Args:
            sala_id: ID de la sala

        Returns:
            Diccionario con datos de la sala o None si no existe
        """
        try:
            async with httpx.AsyncClient(timeout=JavaServiceClient.TIMEOUT) as client:
                response = await client.get(
                    f"{JavaServiceClient.JAVA_SERVICE_URL}/api/salas/{sala_id}"
                )

                if response.status_code == 200:
                    sala_data = response.json()
                    logger.info("✅ Detalles de sala %s obtenidos desde Java Service", sala_id)
                    return sala_data
                else:
                    logger.warning("⚠️ No se pudieron obtener detalles de sala %s", sala_id)
                    return None

        except httpx.RequestError as e:
            logger.error("❌ Error al obtener detalles de sala %s: %s", sala_id, str(e))
            return None

    @staticmethod
    async def check_sala_disponible(sala_id: int) -> bool:
        """
        Verificar si una sala está marcada como disponible en Java.

        Args:
            sala_id: ID de la sala

        Returns:
            True si está disponible, False en caso contrario
        """
        sala_data = await JavaServiceClient.get_sala_details(sala_id)

        if sala_data is None:
            return False

        # Verificar el campo 'disponible'
        is_disponible = sala_data.get("disponible", False)

        if is_disponible:
            logger.info("✅ Sala %s está disponible según Java Service", sala_id)
        else:
            logger.warning("⚠️ Sala %s NO está disponible según Java Service", sala_id)

        return is_disponible

    @staticmethod
    async def get_salas_disponibles() -> list:
        """
        Obtener lista de todas las salas disponibles desde Java.

        Returns:
            Lista de salas disponibles
        """
        try:
            async with httpx.AsyncClient(timeout=JavaServiceClient.TIMEOUT) as client:
                response = await client.get(
                    f"{JavaServiceClient.JAVA_SERVICE_URL}/api/salas/disponibles"
                )
                if response.status_code == 200:
                    salas = response.json()
                    logger.info("✅ %d salas disponibles obtenidas desde Java Service", len(salas))
                    return salas
                else:
                    logger.warning(
                        "⚠️ Error al obtener salas disponibles: %s", response.status_code)
                    return []
        except httpx.RequestError as e:
            logger.error("❌ Error al obtener salas disponibles en Java: %s", e)
            return []

    @staticmethod
    async def check_service_health() -> bool:
        """
        Verificar si el servicio Java está disponible.

        Returns:
            True si el servicio responde, False en caso contrario
        """
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(
                    f"{JavaServiceClient.JAVA_SERVICE_URL}/api/salas"
                )
                is_healthy = response.status_code == 200
                if is_healthy:
                    logger.info("✅ Java Service está disponible y respondiendo")
                else:
                    logger.warning("⚠️ Java Service respondió con status %s", response.status_code)
                return is_healthy
        except httpx.RequestError as e:
            logger.error("❌ Error al chequear salud de Java Service: %s", e)
            return False
