"""Módulo de endpoints de análisis y métricas del sistema de reservas."""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from collections import Counter
from io import BytesIO, StringIO
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import pandas as pd
from app.core.database import get_db
from app.services.analytics_service import AnalyticsService
from app.prediction.prediction_service import PredictionService
from app.auth.dependencies import get_current_user
from app.models.reserva import Reserva
from app.repositories.sala_repository import SalaRepository
from app.repositories.persona_repository import PersonaRepository

router = APIRouter()

@router.get("/dashboard-metrics")
def get_dashboard_metrics(
    days: int = Query(
        30, ge=1, le=365, description="Días hacia atrás para analizar"
    ),
    db: Session = Depends(get_db),
    _current_user = Depends(get_current_user)
):
    """Obtener métricas principales para el dashboard"""
    try:
        ahora_local = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))
        fecha_inicio = ahora_local - timedelta(days=days)

        # Reservas en el período
        reservas = db.query(Reserva).filter(
            Reserva.fecha_hora_inicio >= fecha_inicio.replace(tzinfo=None)
        ).all()

        # 1. Ocupación por sala
        salas = SalaRepository.get_all(db)
        ocupacion_salas = []

        for sala in salas:
            reservas_sala = [r for r in reservas if r.id_sala == sala.id]
            if reservas_sala:
                total_horas = sum(
                    (r.fecha_hora_fin - r.fecha_hora_inicio).total_seconds() / 3600
                    for r in reservas_sala
                )
                horas_promedio = total_horas / len(reservas_sala)
            else:
                horas_promedio = 0

            ocupacion_salas.append({
                "sala": sala.nombre,
                "reservas": len(reservas_sala),
                "horas_promedio": round(horas_promedio, 1)
            })

        # 2. Tendencia de reservas (últimos días)
        tendencia_labels = []
        tendencia_values = []

        for i in range(min(days, 30), -1, -1):
            dia = ahora_local - timedelta(days=i)
            dia_inicio = dia.replace(hour=0, minute=0, second=0, microsecond=0)
            dia_fin = dia.replace(
                hour=23, minute=59, second=59, microsecond=999999
            )

            count = 0
            for r in reservas:
                # Convertir fecha_hora_inicio a timezone aware
                fecha_reserva = r.fecha_hora_inicio.replace(
                    tzinfo=ZoneInfo("America/Argentina/Buenos_Aires")
                ) if r.fecha_hora_inicio.tzinfo is None else r.fecha_hora_inicio
                if dia_inicio <= fecha_reserva <= dia_fin:
                    count += 1

            tendencia_labels.append(dia.strftime("%d/%m"))
            tendencia_values.append(count)

        # 3. Top usuarios (más reservas)
        persona_counts = Counter(r.id_persona for r in reservas if r.id_persona)
        top_usuarios = []

        for persona_id, count in persona_counts.most_common(5):
            persona = PersonaRepository.get_by_id(db, persona_id)
            if persona:
                nombre_completo = (
                    f"{persona.nombre} {persona.apellido or ''}".strip()
                )
                top_usuarios.append({
                    "nombre": nombre_completo,
                    "reservas": count
                })

        # 4. Métricas generales
        reservas_hoy = sum(
            1 for r in reservas
            if r.fecha_hora_inicio.date() == ahora_local.date()
        )

        salas_disponibles = sum(1 for s in salas if s.disponible)

        # Calcular ocupación promedio
        if reservas:
            total_horas_reservadas = sum(
                (r.fecha_hora_fin - r.fecha_hora_inicio).total_seconds() / 3600
                for r in reservas
            )
            horas_disponibles = len(salas) * 24 * days
            ocupacion_promedio = (
                total_horas_reservadas / horas_disponibles * 100
            ) if horas_disponibles > 0 else 0
        else:
            ocupacion_promedio = 0

        return {
            "ocupacion_salas": ocupacion_salas,
            "tendencia_reservas": {
                "labels": tendencia_labels,
                "values": tendencia_values
            },
            "top_usuarios": top_usuarios,
            "metricas": {
                "reservas_hoy": reservas_hoy,
                "ocupacion_promedio": round(ocupacion_promedio, 1),
                "salas_disponibles": salas_disponibles
            }
        }
    except (ValueError, KeyError, AttributeError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener métricas: {str(e)}"
        ) from e

@router.get("/ocupacion-prediccion")
def get_prediccion_ocupacion(
    dias: int = Query(
        7, ge=1, le=30, description="Días adelante para predecir"
    ),
    db: Session = Depends(get_db),
    _current_user = Depends(get_current_user)
):
    """Predicción de ocupación de salas"""
    try:
        analytics_service = AnalyticsService(db)
        return analytics_service.get_prediccion_ocupacion(dias)
    except (ValueError, KeyError, AttributeError, RuntimeError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar predicciones: {str(e)}"
        ) from e

@router.get("/inventario-metrics")
def get_inventario_metrics(
    db: Session = Depends(get_db),
    _current_user = Depends(get_current_user)
):
    """Métricas de inventario y artículos"""
    try:
        analytics_service = AnalyticsService(db)
        return analytics_service.get_metricas_inventario()
    except (ValueError, KeyError, AttributeError, RuntimeError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener métricas de inventario: {str(e)}"
        ) from e

@router.get("/export-report")
def export_report(
    export_format: str = Query("json", pattern="^(json|csv|excel)$"),
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    _current_user = Depends(get_current_user)
):
    """Exportar reportes en diferentes formatos (JSON, CSV, Excel)"""
    try:
        analytics_service = AnalyticsService(db)
        data = analytics_service.get_ocupacion_dashboard(days)

        # Agregar más datos para el reporte completo
        ahora_local = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))
        fecha_inicio = ahora_local - timedelta(days=days)

        # Obtener reservas del período
        reservas = db.query(Reserva).filter(
            Reserva.fecha_hora_inicio >= fecha_inicio.replace(tzinfo=None)
        ).all()

        # Preparar datos para el reporte
        reporte_data = {
            'metadata': {
                'fecha_generacion': ahora_local.isoformat(),
                'periodo_dias': days,
                'fecha_inicio': fecha_inicio.isoformat(),
                'fecha_fin': ahora_local.isoformat()
            },
            'metricas_generales': data,
            'reservas': []
        }

        # Agregar datos de reservas
        for reserva in reservas:
            # Determinar si la reserva está activa basándose en las fechas
            ahora = datetime.now()
            es_activa = reserva.fecha_hora_inicio <= ahora <= reserva.fecha_hora_fin
            es_pasada = ahora > reserva.fecha_hora_fin

            estado_calculado = (
                'activa' if es_activa else (
                    'completada' if es_pasada else 'pendiente'
                )
            )

            reporte_data['reservas'].append({
                'id': reserva.id,
                'fecha_inicio': (
                    reserva.fecha_hora_inicio.isoformat()
                    if reserva.fecha_hora_inicio else None
                ),
                'fecha_fin': (
                    reserva.fecha_hora_fin.isoformat()
                    if reserva.fecha_hora_fin else None
                ),
                'id_persona': reserva.id_persona,
                'id_sala': reserva.id_sala,
                'id_articulo': reserva.id_articulo,
                'tipo': 'sala' if reserva.id_sala else 'articulo',
                'estado': estado_calculado,
                'duracion_horas': round(
                    (reserva.fecha_hora_fin - reserva.fecha_hora_inicio
                     ).total_seconds() / 3600, 2
                )
            })

        # Exportar según el formato solicitado
        if export_format == "csv":
            # Convertir a DataFrame
            df = pd.DataFrame(reporte_data['reservas'])
            if df.empty:
                df = pd.DataFrame([{
                    'mensaje': 'No hay reservas en el período seleccionado'
                }])

            # Crear CSV en memoria
            output = StringIO()
            df.to_csv(output, index=False, encoding='utf-8')
            output.seek(0)

            filename = (
                f"reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            return StreamingResponse(
                iter([output.getvalue()]),
                media_type="text/csv",
                headers={
                    "Content-Disposition": f"attachment; filename={filename}"
                }
            )

        elif export_format == "excel":
            # Crear Excel en memoria
            output = BytesIO()

            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # Hoja de métricas generales
                metricas_df = pd.DataFrame([reporte_data['metricas_generales']])
                metricas_df.to_excel(writer, sheet_name='Métricas', index=False)

                # Hoja de reservas
                reservas_df = pd.DataFrame(reporte_data['reservas'])
                if reservas_df.empty:
                    reservas_df = pd.DataFrame([{
                        'mensaje': 'No hay reservas en el período seleccionado'
                    }])
                reservas_df.to_excel(writer, sheet_name='Reservas', index=False)

                # Hoja de metadata
                metadata_df = pd.DataFrame([reporte_data['metadata']])
                metadata_df.to_excel(writer, sheet_name='Info', index=False)

            output.seek(0)

            filename = (
                f"reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            media_type = (
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
            return StreamingResponse(
                iter([output.getvalue()]),
                media_type=media_type,
                headers={
                    "Content-Disposition": f"attachment; filename={filename}"
                }
            )

        # Formato JSON por defecto
        return reporte_data

    except (ValueError, KeyError, AttributeError, RuntimeError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al exportar reporte: {str(e)}"
        ) from e


# ========== NUEVOS ENDPOINTS DE PREDICCIÓN ==========

@router.get("/predictions/weekly-demand")
def get_weekly_demand_predictions(
    dias: int = Query(
        7, ge=1, le=30, description="Días adelante para predecir"
    ),
    db: Session = Depends(get_db),
    _current_user = Depends(get_current_user)
):
    """
    Predicción avanzada de demanda semanal.

    Utiliza análisis de patrones históricos, tendencias y estacionalidad
    para predecir la demanda de reservas en los próximos días.
    """
    try:
        prediction_service = PredictionService(db)
        resultado = prediction_service.predict_weekly_demand(dias)
        # Transformar nombres de campos para compatibilidad con frontend
        predicciones_transformadas = []
        for pred in resultado.get("predicciones", []):
            predicciones_transformadas.append({
                "fecha": pred["fecha"],
                "dia_semana": pred["dia_semana"],
                # Mapear prediccion_reservas -> demanda_estimada
                "demanda_estimada": pred["prediccion_reservas"],
                # Mapear confianza -> nivel_confianza
                "nivel_confianza": pred["confianza"],
                "nivel_demanda": pred["nivel_demanda"],
                "recomendacion": pred.get("recomendacion", "")
            })

        # Transformar metadata
        metadata = resultado.get("metadata", {})
        metadata_transformada = {
            "total_reservas_historicas": metadata.get(
                "total_reservas_historicas"
            ),
            "dias_analizados": metadata.get("dias_historicos"),
            "tendencia_general": metadata.get("tendencia"),
            "confianza_promedio": (
                sum(p["confianza"] for p in resultado.get(
                    "predicciones", [])) / len(resultado.get("predicciones", []))
                if resultado.get("predicciones") else 0
            )
        }

        return {
            "predicciones": predicciones_transformadas,
            "metadata": metadata_transformada
        }
    except (ValueError, KeyError, AttributeError, RuntimeError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar predicciones de demanda: {str(e)}"
        ) from e


@router.get("/predictions/peak-hours")
def get_peak_hours_predictions(
    dias: int = Query(
        30, ge=7, le=90, description="Días históricos a analizar"
    ),
    db: Session = Depends(get_db),
    _current_user = Depends(get_current_user)
):
    """
    Identifica horarios pico de reservas.

    Analiza patrones históricos para determinar qué horas del día
    tienen mayor demanda por cada día de la semana.
    """
    try:
        prediction_service = PredictionService(db)
        return prediction_service.predict_peak_hours(dias)
    except (ValueError, KeyError, AttributeError, RuntimeError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al analizar horarios pico: {str(e)}"
        ) from e


@router.get("/predictions/anomalies")
def detect_demand_anomalies(
    dias: int = Query(30, ge=7, le=90, description="Días a analizar"),
    db: Session = Depends(get_db),
    _current_user = Depends(get_current_user)
):
    """
    Detecta anomalías en la demanda.

    Identifica días con ocupación inusualmente alta o baja
    usando análisis estadístico.
    """
    try:
        prediction_service = PredictionService(db)
        return prediction_service.detect_anomalies(dias)
    except (ValueError, KeyError, AttributeError, RuntimeError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al detectar anomalías: {str(e)}"
        ) from e


@router.get("/predictions/capacity-recommendations")
def get_capacity_recommendations(
    dias: int = Query(
        7, ge=1, le=30, description="Días adelante para analizar"
    ),
    db: Session = Depends(get_db),
    _current_user = Depends(get_current_user)
):
    """
    Recomendaciones de capacidad.

    Basado en predicciones de demanda, sugiere cuántas salas
    deberían estar disponibles cada día.
    """
    try:
        prediction_service = PredictionService(db)
        return prediction_service.recommend_capacity(dias)
    except (ValueError, KeyError, AttributeError, RuntimeError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar recomendaciones: {str(e)}"
        ) from e
