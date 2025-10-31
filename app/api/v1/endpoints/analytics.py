from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.services.analytics_service import AnalyticsService
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/dashboard-metrics")
def get_dashboard_metrics(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener métricas principales para el dashboard"""
    analytics_service = AnalyticsService(db)
    return analytics_service.get_ocupacion_dashboard(days)

@router.get("/ocupacion-prediccion")
def get_prediccion_ocupacion(
    dias: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Predicción de ocupación de salas"""
    analytics_service = AnalyticsService(db)
    return analytics_service.get_prediccion_ocupacion(dias)

@router.get("/inventario-metrics")
def get_inventario_metrics(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Métricas de inventario y artículos"""
    analytics_service = AnalyticsService(db)
    return analytics_service.get_metricas_inventario()

@router.get("/export-report")
def export_report(
    format: str = Query("json", regex="^(json|csv|excel)$"),
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Exportar reportes en diferentes formatos"""
    analytics_service = AnalyticsService(db)
    data = analytics_service.get_ocupacion_dashboard(days)
    
    if format == "csv":
        # Implementar exportación CSV
        pass
    elif format == "excel":
        # Implementar exportación Excel
        pass
    
    return data
