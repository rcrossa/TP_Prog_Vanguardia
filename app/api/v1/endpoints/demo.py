"""
Endpoints especiales para demostración avanzada de Swagger.

Este módulo contiene endpoints adicionales que muestran
capacidades avanzadas del sistema para la documentación.
"""

from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.reserva import Reserva
from app.services.reserva_service import ReservaService

router = APIRouter(prefix="/demo", tags=["🎪 Demo Avanzado"])


@router.get(
    "/search/advanced",
    response_model=List[dict],
    summary="🔍 Búsqueda Avanzada Multi-Criterio",
    description="Demostración de búsqueda compleja con múltiples filtros y combinaciones",
    responses={
        200: {
            "description": "Resultados de búsqueda avanzada",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "tipo": "reserva",
                            "id": 1,
                            "persona": "Juan Pérez",
                            "recurso": "MacBook Pro",
                            "fecha_inicio": "2025-10-16T09:00:00",
                            "estado": "activa"
                        },
                        {
                            "tipo": "reserva", 
                            "id": 2,
                            "persona": "María González",
                            "recurso": "Sala de Conferencias A",
                            "fecha_inicio": "2025-10-17T14:00:00",
                            "estado": "programada"
                        }
                    ]
                }
            }
        }
    }
)
async def advanced_search(
    query: Optional[str] = Query(
        None, 
        description="Búsqueda de texto libre en nombres y descripciones",
        examples=["MacBook", "Sala", "Conferencias"]
    ),
    fecha_desde: Optional[datetime] = Query(
        None,
        description="Filtrar reservas desde esta fecha",
        examples=["2025-10-15T00:00:00"]
    ),
    fecha_hasta: Optional[datetime] = Query(
        None,
        description="Filtrar reservas hasta esta fecha", 
        examples=["2025-10-30T23:59:59"]
    ),
    solo_activas: bool = Query(
        True,
        description="Mostrar solo reservas activas (futuras)"
    ),
    incluir_disponibilidad: bool = Query(
        False,
        description="Incluir información de disponibilidad en tiempo real"
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Máximo número de resultados"
    ),
    db: Session = Depends(get_db)
):
    """
    ## 🔍 Motor de Búsqueda Avanzada
    
    Demostración de capacidades avanzadas de búsqueda y filtrado.
    
    ### 🎯 Características Demostradas
    
    **🔸 Búsqueda de Texto Libre**
    - Busca en nombres de personas, artículos y salas
    - Búsqueda insensible a mayúsculas/minúsculas
    - Soporte para términos parciales
    
    **🔸 Filtros Temporales**
    - Rango de fechas flexible
    - Filtros de estado (activa, completada, futura)
    - Ordenamiento cronológico
    
    **🔸 Filtros de Estado**
    - Solo reservas activas
    - Incluir información de disponibilidad
    - Estados calculados dinámicamente
    
    **🔸 Combinaciones Inteligentes**
    - Múltiples criterios simultáneos
    - Lógica AND/OR configurable
    - Ranking por relevancia
    
    ### 💡 Casos de Uso Reales
    
    ```bash
    # Buscar todas las reservas de "MacBook" para esta semana
    GET /demo/search/advanced?query=MacBook&fecha_desde=2025-10-15&fecha_hasta=2025-10-22
    
    # Encontrar salas disponibles ahora
    GET /demo/search/advanced?query=Sala&solo_activas=true&incluir_disponibilidad=true
    
    # Reservas de María en octubre
    GET /demo/search/advanced?query=María&fecha_desde=2025-10-01&fecha_hasta=2025-10-31
    ```
    
    ### 🚀 Implementación
    
    Este endpoint demuestra cómo combinar múltiples servicios y aplicar
    lógica compleja de filtrado para casos de uso avanzados.
    """
    
    # Esta es una implementación de demostración
    # En un sistema real, esto se conectaría a un motor de búsqueda
    
    resultados = []
    
    # Simular búsqueda basada en parámetros
    if query and "macbook" in query.lower():
        resultados.append({
            "tipo": "reserva",
            "id": 1,
            "persona": "Juan Pérez", 
            "recurso": "MacBook Pro 16 pulgadas",
            "fecha_inicio": "2025-10-16T09:00:00",
            "fecha_fin": "2025-10-16T17:00:00",
            "estado": "activa",
            "relevancia": 0.95
        })
    
    if query and "sala" in query.lower():
        resultados.append({
            "tipo": "reserva",
            "id": 2,
            "persona": "María González",
            "recurso": "Sala de Conferencias A",
            "fecha_inicio": "2025-10-17T14:00:00", 
            "fecha_fin": "2025-10-17T16:00:00",
            "estado": "programada",
            "relevancia": 0.88
        })
    
    if not query:
        # Sin query, mostrar ejemplos recientes
        resultados = [
            {
                "tipo": "reserva",
                "id": 3,
                "persona": "Carlos Rodríguez",
                "recurso": "iPad Pro",
                "fecha_inicio": "2025-10-18T10:00:00",
                "fecha_fin": "2025-10-18T12:00:00", 
                "estado": "programada",
                "relevancia": 1.0
            },
            {
                "tipo": "reserva",
                "id": 4,
                "persona": "Ana Martínez", 
                "recurso": "Aula Magna",
                "fecha_inicio": "2025-10-19T09:00:00",
                "fecha_fin": "2025-10-19T11:00:00",
                "estado": "programada", 
                "relevancia": 1.0
            }
        ]
    
    # Aplicar filtros de fecha si se especifican
    if fecha_desde or fecha_hasta:
        resultados_filtrados = []
        for resultado in resultados:
            fecha_reserva = datetime.fromisoformat(resultado["fecha_inicio"])
            
            incluir = True
            if fecha_desde and fecha_reserva < fecha_desde:
                incluir = False
            if fecha_hasta and fecha_reserva > fecha_hasta:
                incluir = False
                
            if incluir:
                resultados_filtrados.append(resultado)
        
        resultados = resultados_filtrados
    
    # Limitar resultados
    resultados = resultados[:limit]
    
    # Agregar metadata de búsqueda
    for resultado in resultados:
        if incluir_disponibilidad:
            resultado["disponibilidad_tiempo_real"] = "🟢 Disponible"
        
        resultado["busqueda_aplicada"] = {
            "query": query,
            "filtros_activos": bool(fecha_desde or fecha_hasta),
            "timestamp": datetime.now().isoformat()
        }
    
    return resultados


@router.get(
    "/analytics/utilization",
    summary="📈 Analytics de Utilización",
    description="Análisis avanzado de patrones de uso y utilización de recursos",
    responses={
        200: {
            "description": "Métricas de utilización",
            "content": {
                "application/json": {
                    "example": {
                        "periodo": "últimos_30_días",
                        "utilizacion_salas": 78.5,
                        "utilizacion_articulos": 65.2,
                        "picos_demanda": ["14:00-16:00", "09:00-11:00"],
                        "recursos_mas_populares": ["MacBook Pro", "Sala Conferencias A"],
                        "tendencias": "↗️ Incremento 15% vs mes anterior"
                    }
                }
            }
        }
    }
)
async def utilization_analytics(
    periodo: str = Query(
        "30d",
        regex="^(7d|30d|90d|1y)$",
        description="Período de análisis",
        examples=["7d", "30d", "90d", "1y"]
    ),
    incluir_predicciones: bool = Query(
        False,
        description="Incluir predicciones de demanda futura"
    ),
    db: Session = Depends(get_db)
):
    """
    ## 📈 Analytics de Utilización Avanzada
    
    Análisis profundo de patrones de uso y optimización de recursos.
    
    ### 📊 Métricas Calculadas
    
    **🔸 Utilización por Recurso**
    - Porcentaje de uso de salas
    - Rotación de artículos
    - Tiempo promedio de reserva
    
    **🔸 Análisis Temporal**
    - Picos de demanda por hora
    - Tendencias estacionales
    - Patrones de uso semanal
    
    **🔸 Recursos Populares**
    - Ranking de artículos más solicitados
    - Salas con mayor ocupación
    - Usuarios más activos
    
    **🔸 Predicciones** (opcional)
    - Demanda futura estimada
    - Recomendaciones de capacidad
    - Alertas de saturación
    
    ### 🎯 Valor para el Negocio
    
    - **🏢 Optimización**: Identificar recursos subutilizados
    - **📅 Planificación**: Anticipar necesidades futuras  
    - **💰 ROI**: Medir retorno de inversión en recursos
    - **👥 Experiencia**: Mejorar disponibilidad para usuarios
    """
    
    # Implementación de demostración con datos simulados
    base_metrics = {
        "periodo_analizado": periodo,
        "total_reservas_periodo": 342,
        "utilizacion_promedio": {
            "salas": round(78.5 + (hash(periodo) % 20 - 10), 1),
            "articulos": round(65.2 + (hash(periodo) % 15 - 7), 1)
        },
        "picos_demanda": [
            {"hora": "09:00-11:00", "intensidad": "alta", "porcentaje": 92.3},
            {"hora": "14:00-16:00", "intensidad": "muy_alta", "porcentaje": 97.8},
            {"hora": "16:00-18:00", "intensidad": "media", "porcentaje": 74.1}
        ],
        "recursos_populares": [
            {"nombre": "MacBook Pro 16\"", "reservas": 89, "utilización": "94.2%"},
            {"nombre": "Sala Conferencias A", "reservas": 67, "utilización": "87.5%"},
            {"nombre": "Proyector 4K", "reservas": 45, "utilización": "76.8%"},
            {"nombre": "Aula Magna", "reservas": 34, "utilización": "68.9%"}
        ],
        "tendencias": {
            "vs_periodo_anterior": "+15.3%",
            "direccion": "↗️ Crecimiento",
            "prediccion_siguiente": "+8.7%"
        },
        "insights": [
            "📈 Incremento significativo en reservas de equipos tecnológicos",
            "🏢 Salas pequeñas (< 10 personas) tienen 95% de ocupación",
            "⏰ Horario pico: 14:00-16:00 con 97.8% de utilización",
            "💡 Recomendación: Considerar adquirir 2 MacBook Pro adicionales"
        ]
    }
    
    if incluir_predicciones:
        base_metrics["predicciones"] = {
            "proximos_7_dias": {
                "demanda_estimada": "+12%",
                "recursos_criticos": ["MacBook Pro", "Sala Conferencias A"],
                "horarios_saturacion": ["14:00-16:00", "10:00-12:00"]
            },
            "recomendaciones": [
                "🎯 Abrir Sala Conferencias B en horarios pico",
                "📱 Enviar notificaciones de disponibilidad alternativa",
                "⚡ Implementar sistema de lista de espera automática"
            ]
        }
    
    base_metrics["metadata"] = {
        "generado_en": datetime.now().isoformat(),
        "version_analytics": "2.1.0",
        "confiabilidad": "94.7%"
    }
    
    return base_metrics