"""
Endpoint de demostración para probar integración con Java Service.

Este endpoint muestra cómo Python puede consultar datos desde Java.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.java_client import JavaServiceClient
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/integration/health")
async def check_java_service_health():
    """
    🔗 ENDPOINT DE INTEGRACIÓN: Verificar si el Java Service está disponible.
    
    Este endpoint hace una llamada al Java Service para verificar su estado.
    """
    is_healthy = await JavaServiceClient.check_service_health()
    
    if is_healthy:
        return {
            "status": "healthy",
            "message": "✅ Java Service está disponible y respondiendo",
            "java_service_url": "http://localhost:8080"
        }
    else:
        return {
            "status": "unhealthy",
            "message": "❌ Java Service NO está disponible",
            "java_service_url": "http://localhost:8080"
        }


@router.get("/integration/salas-desde-java")
async def get_salas_from_java():
    """
    🔗 ENDPOINT DE INTEGRACIÓN: Obtener salas disponibles desde Java Service.
    
    Este endpoint consulta directamente al Java Service en lugar de usar la DB local.
    """
    logger.info("🔗 Consultando salas disponibles desde Java Service...")
    
    salas = await JavaServiceClient.get_salas_disponibles()
    
    if not salas:
        return {
            "message": "⚠️ No se pudieron obtener salas desde Java Service",
            "salas": [],
            "source": "java-service (error o sin datos)"
        }
    
    return {
        "message": f"✅ {len(salas)} salas obtenidas desde Java Service",
        "salas": salas,
        "source": "java-service",
        "count": len(salas)
    }


@router.get("/integration/sala/{sala_id}/validar")
async def validate_sala_with_java(sala_id: int):
    """
    🔗 ENDPOINT DE INTEGRACIÓN: Validar una sala específica contra Java Service.
    
    Args:
        sala_id: ID de la sala a validar
    """
    logger.info(f"🔗 Validando sala {sala_id} contra Java Service...")
    
    # Verificar si existe
    exists = await JavaServiceClient.validate_sala_exists(sala_id)
    
    if not exists:
        raise HTTPException(
            status_code=404,
            detail=f"❌ Sala {sala_id} no encontrada en Java Service"
        )
    
    # Obtener detalles
    sala_details = await JavaServiceClient.get_sala_details(sala_id)
    
    # Verificar disponibilidad
    is_disponible = await JavaServiceClient.check_sala_disponible(sala_id)
    
    return {
        "message": f"✅ Sala {sala_id} validada exitosamente",
        "exists": exists,
        "disponible": is_disponible,
        "details": sala_details,
        "source": "java-service"
    }


@router.get("/integration/articulo/{articulo_id}/validar")
async def validate_articulo_with_java(articulo_id: int):
    """
    🔗 ENDPOINT DE INTEGRACIÓN: Validar un artículo específico contra Java Service.
    
    Args:
        articulo_id: ID del artículo a validar
    """
    logger.info(f"🔗 Validando artículo {articulo_id} contra Java Service...")
    
    # Verificar si existe
    exists = await JavaServiceClient.validate_articulo_exists(articulo_id)
    
    if not exists:
        raise HTTPException(
            status_code=404,
            detail=f"❌ Artículo {articulo_id} no encontrado en Java Service"
        )
    
    # Obtener detalles
    articulo_details = await JavaServiceClient.get_articulo_details(articulo_id)
    
    return {
        "message": f"✅ Artículo {articulo_id} validado exitosamente",
        "exists": exists,
        "details": articulo_details,
        "source": "java-service"
    }


@router.get("/integration/demo")
async def integration_demo():
    """
    🔗 ENDPOINT DE DEMOSTRACIÓN: Mostrar ejemplos de integración Python ↔ Java.
    """
    # Verificar health del Java Service
    java_healthy = await JavaServiceClient.check_service_health()
    
    # Intentar obtener algunas salas
    salas = await JavaServiceClient.get_salas_disponibles()
    
    return {
        "title": "🔗 Demostración de Integración Python ↔ Java",
        "description": "Este endpoint muestra cómo Python se comunica con Java via HTTP",
        "java_service": {
            "url": "http://localhost:8080",
            "status": "✅ Disponible" if java_healthy else "❌ No disponible",
            "swagger": "http://localhost:8080/swagger-ui.html"
        },
        "examples": {
            "health_check": "/api/v1/integration/health",
            "get_salas_from_java": "/api/v1/integration/salas-desde-java",
            "validate_sala": "/api/v1/integration/sala/{sala_id}/validar",
            "validate_articulo": "/api/v1/integration/articulo/{articulo_id}/validar"
        },
        "sample_data": {
            "salas_count": len(salas) if salas else 0,
            "salas_disponibles": salas[:3] if salas else []  # Primeras 3 salas
        }
    }
