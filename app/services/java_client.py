"""
Cliente HTTP para comunicación con el servicio Java.

Este módulo maneja todas las llamadas HTTP al microservicio Java
que gestiona Salas y Artículos.
"""

import logging
from typing import Any, Dict, Optional

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class JavaServiceClient:
    """Cliente para comunicación con el servicio Java."""

    # URL base del servicio Java
    JAVA_SERVICE_URL = "http://localhost:8080"

    # Timeout para las peticiones (en segundos)
    TIMEOUT = 5.0

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
                    logger.info(
                        f"✅ Sala {sala_id} validada exitosamente desde Java Service"
                    )
                    return True
                elif response.status_code == 404:
                    logger.warning(f"⚠️ Sala {sala_id} no encontrada en Java Service")
                    return False
                else:
                    logger.error(
                        f"❌ Error al validar sala {sala_id}: Status {response.status_code}"
                    )
                    return False

        except httpx.TimeoutException:
            logger.error(f"⏱️ Timeout al conectar con Java Service para sala {sala_id}")
            # Si el servicio Java no está disponible, fallback a validación local
            return False
        except httpx.ConnectError:
            logger.error(f"🔌 No se pudo conectar con Java Service para sala {sala_id}")
            # Si el servicio Java no está disponible, fallback a validación local
            return False
        except Exception as e:
            logger.error(f"❌ Error inesperado al validar sala {sala_id}: {str(e)}")
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
                    logger.info(
                        f"✅ Detalles de sala {sala_id} obtenidos desde Java Service"
                    )
                    return sala_data
                else:
                    logger.warning(
                        f"⚠️ No se pudieron obtener detalles de sala {sala_id}"
                    )
                    return None

        except Exception as e:
            logger.error(f"❌ Error al obtener detalles de sala {sala_id}: {str(e)}")
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
            logger.info(f"✅ Sala {sala_id} está disponible según Java Service")
        else:
            logger.warning(f"⚠️ Sala {sala_id} NO está disponible según Java Service")

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
                    logger.info(
                        f"✅ {len(salas)} salas disponibles obtenidas desde Java Service"
                    )
                    return salas
                else:
                    logger.warning(
                        f"⚠️ Error al obtener salas disponibles: {response.status_code}"
                    )
                    return []

        except Exception as e:
            logger.error(f"❌ Error al obtener salas disponibles: {str(e)}")
            return []

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
                    logger.info(
                        f"✅ Artículo {articulo_id} validado exitosamente desde Java Service"
                    )
                    return True
                elif response.status_code == 404:
                    logger.warning(
                        f"⚠️ Artículo {articulo_id} no encontrado en Java Service"
                    )
                    return False
                else:
                    logger.error(
                        f"❌ Error al validar artículo {articulo_id}: Status {response.status_code}"
                    )
                    return False

        except Exception as e:
            logger.error(f"❌ Error al validar artículo {articulo_id}: {str(e)}")
            return False

    @staticmethod
    async def get_articulo_details(articulo_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtener detalles completos de un artículo desde el servicio Java.

        Args:
            articulo_id: ID del artículo

        Returns:
            Diccionario con datos del artículo o None si no existe
        """
        try:
            async with httpx.AsyncClient(timeout=JavaServiceClient.TIMEOUT) as client:
                response = await client.get(
                    f"{JavaServiceClient.JAVA_SERVICE_URL}/api/articulos/{articulo_id}"
                )

                if response.status_code == 200:
                    articulo_data = response.json()
                    logger.info(
                        f"✅ Detalles de artículo {articulo_id} obtenidos desde Java Service"
                    )
                    return articulo_data
                else:
                    logger.warning(
                        f"⚠️ No se pudieron obtener detalles de artículo {articulo_id}"
                    )
                    return None

        except Exception as e:
            logger.error(
                f"❌ Error al obtener detalles de artículo {articulo_id}: {str(e)}"
            )
            return None

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
                    logger.warning(
                        f"⚠️ Java Service respondió con status {response.status_code}"
                    )

                return is_healthy

        except Exception as e:
            logger.error(f"❌ Java Service NO está disponible: {str(e)}")
            return False
