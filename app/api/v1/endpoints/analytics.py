from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.services.analytics_service import AnalyticsService
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/dashboard-metrics")
def get_dashboard_metrics(
    days: int = Query(30, ge=1, le=365, description="Días hacia atrás para analizar"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener métricas principales para el dashboard"""
    try:
        analytics_service = AnalyticsService(db)
        return analytics_service.get_ocupacion_dashboard(days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener métricas: {str(e)}")

@router.get("/ocupacion-prediccion")
def get_prediccion_ocupacion(
    dias: int = Query(7, ge=1, le=30, description="Días adelante para predecir"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Predicción de ocupación de salas"""
    try:
        analytics_service = AnalyticsService(db)
        return analytics_service.get_prediccion_ocupacion(dias)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar predicciones: {str(e)}")

@router.get("/inventario-metrics")
def get_inventario_metrics(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Métricas de inventario y artículos"""
    try:
        analytics_service = AnalyticsService(db)
        return analytics_service.get_metricas_inventario()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener métricas de inventario: {str(e)}")

@router.get("/export-report")
def export_report(
    format: str = Query("json", pattern="^(json|csv|excel)$"),
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Exportar reportes en diferentes formatos"""
    try:
        analytics_service = AnalyticsService(db)
        data = analytics_service.get_ocupacion_dashboard(days)
        
        if format == "csv":
            # TODO: Implementar exportación CSV
            raise HTTPException(status_code=501, detail="Exportación CSV en desarrollo")
        elif format == "excel":
            # TODO: Implementar exportación Excel
            raise HTTPException(status_code=501, detail="Exportación Excel en desarrollo")
        
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al exportar reporte: {str(e)}")
