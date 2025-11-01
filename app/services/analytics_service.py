from datetime import datetime, timedelta
from typing import Dict
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from app.models.reserva import Reserva
from app.models.sala import Sala
from app.models.articulo import Articulo
from app.models.persona import Persona

class AnalyticsService:
    """Servicio para análisis y métricas del sistema de reservas."""
    def __init__(self, db: Session):
        self.db = db

    def get_ocupacion_dashboard(self, days: int = 30) -> Dict:
        """Métricas principales para el dashboard"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        # Total de reservas en el periodo
        total_reservas = self.db.query(func.count(Reserva.id)).filter(
            Reserva.fecha_hora_inicio >= start_date,
            Reserva.fecha_hora_inicio <= end_date
        ).scalar() or 0
        # Ocupación por sala
        ocupacion_salas = self.db.query(
            Sala.nombre,
            func.count(Reserva.id).label('total_reservas'),
            func.avg(
                func.extract('epoch', Reserva.fecha_hora_fin - Reserva.fecha_hora_inicio) / 3600
            ).label('horas_promedio')
        ).outerjoin(Reserva, and_(
            Reserva.id_sala == Sala.id,
            Reserva.fecha_hora_inicio >= start_date,
            Reserva.fecha_hora_inicio <= end_date
        )).group_by(Sala.id, Sala.nombre).all()
        # Tendencia de reservas por día
        reservas_por_dia = self.db.query(
            func.date(Reserva.fecha_hora_inicio).label('fecha'),
            func.count(Reserva.id).label('cantidad')
        ).filter(
            Reserva.fecha_hora_inicio >= start_date,
            Reserva.fecha_hora_inicio <= end_date
        ).group_by(func.date(Reserva.fecha_hora_inicio)).order_by('fecha').all()
        # Top usuarios
        top_usuarios = self.db.query(
            Persona.nombre,
            Persona.email,
            func.count(Reserva.id).label('total_reservas')
        ).join(Reserva).filter(
            Reserva.fecha_hora_inicio >= start_date,
            Reserva.fecha_hora_inicio <= end_date
        ).group_by(Persona.id, Persona.nombre, Persona.email).order_by(
            desc('total_reservas')
        ).limit(5).all()
        # Reservas de hoy
        today = datetime.utcnow().date()
        reservas_hoy = self.db.query(func.count(Reserva.id)).filter(
            func.date(Reserva.fecha_hora_inicio) == today
        ).scalar() or 0
        # Salas disponibles ahora
        now = datetime.utcnow()
        salas_ocupadas = self.db.query(func.count(func.distinct(Reserva.id_sala))).filter(
            Reserva.fecha_hora_inicio <= now,
            Reserva.fecha_hora_fin >= now
        ).scalar() or 0
        total_salas = self.db.query(func.count(Sala.id)).scalar() or 0
        salas_disponibles = total_salas - salas_ocupadas
        return {
            'metricas_principales': {
               'total_reservas': total_reservas,
               'reservas_hoy': reservas_hoy,
               'salas_disponibles': salas_disponibles,
               'total_salas': total_salas,
               'ocupacion_porcentaje': round((salas_ocupadas / total_salas * 100) 
                                             if total_salas > 0 else 0, 1)
            },
            'ocupacion_salas': [
                {
                    'sala': sala.nombre,
                    'reservas': sala.total_reservas or 0,
                    'horas_promedio': round(float(sala.horas_promedio or 0), 1)
                } for sala in ocupacion_salas
            ],
            'tendencia_reservas': [
                {
                    'fecha': reserva.fecha.strftime('%Y-%m-%d') 
                    if hasattr(reserva.fecha, 'strftime') else str(reserva.fecha),
                    'cantidad': reserva.cantidad
                } for reserva in reservas_por_dia
            ],
            'top_usuarios': [
                {
                    'nombre': usuario.nombre,
                    'email': usuario.email,
                    'reservas': usuario.total_reservas
                } for usuario in top_usuarios
            ]
        }
    def get_prediccion_ocupacion(self, dias_adelante: int = 7) -> Dict:
        """Predicción de ocupación basada en patrones históricos"""
        # Calcular promedio de reservas por día de la semana
        patron_semanal = self.db.query(
            func.extract('dow', Reserva.fecha_hora_inicio).label('dia_semana'),
            func.count(Reserva.id).label('total_reservas')
        ).group_by(
            func.extract('dow', Reserva.fecha_hora_inicio)
        ).all()

        # Crear diccionario de patrones
        patrones = {int(p.dia_semana): p.total_reservas for p in patron_semanal}

        # Generar predicciones
        predicciones = []
        today = datetime.utcnow().date()

        for i in range(1, dias_adelante + 1):
            fecha_pred = today + timedelta(days=i)
            dia_semana = fecha_pred.weekday()

            # Domingo = 6 en Python, pero PostgreSQL usa 0
            dia_semana_pg = (dia_semana + 1) % 7

            prediccion = patrones.get(dia_semana_pg, 0)

            predicciones.append({
                'fecha': fecha_pred.strftime('%Y-%m-%d'),
                'dia_semana': ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'][dia_semana],
                'prediccion_reservas': prediccion,
                'confianza': 0.75 if prediccion > 0 else 0.3
            })

        return {'predicciones': predicciones}

    def get_metricas_inventario(self) -> Dict:
        """Métricas de inventario y artículos"""
        # Stock total
        total_articulos = self.db.query(func.count(Articulo.id)).scalar() or 0
        stock_total = self.db.query(func.sum(Articulo.cantidad)).scalar() or 0

        # Stock crítico (menos de 5 unidades)
        stock_critico = self.db.query(Articulo).filter(
            Articulo.cantidad < 5
        ).all()

        # Artículos más utilizados (basado en relaciones con reservas)
        # Nota: Esto requiere que tengas una tabla de asociación entre Reserva y Articulo
        articulos_lista = self.db.query(Articulo).limit(10).all()

        return {
            'resumen': {
                'total_articulos': total_articulos,
                'stock_total': stock_total,
                'items_criticos': len(stock_critico)
            },
            'stock_critico': [
                {
                    'id': art.id,
                    'nombre': art.nombre,
                    'cantidad': art.cantidad,
                    'descripcion': art.descripcion
                } for art in stock_critico
            ],
            'articulos': [
                {
                    'id': art.id,
                    'nombre': art.nombre,
                    'cantidad': art.cantidad,
                    'descripcion': art.descripcion
                } for art in articulos_lista
            ]
        }
