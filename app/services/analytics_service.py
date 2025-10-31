from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from app.models.reserva import Reserva
from app.models.sala import Sala
from app.models.articulo import Articulo
from app.models.persona import Persona

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_ocupacion_dashboard(self, days: int = 30) -> Dict:
        """Métricas principales para el dashboard"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Ocupación por sala
        ocupacion_salas = self.db.query(
            Sala.nombre,
            func.count(Reserva.id).label('total_reservas'),
            func.avg(
                func.extract('epoch', Reserva.fecha_fin - Reserva.fecha_inicio) / 3600
            ).label('horas_promedio')
        ).outerjoin(Reserva).filter(
            or_(Reserva.fecha_inicio == None, 
                and_(Reserva.fecha_inicio >= start_date, Reserva.fecha_inicio <= end_date))
        ).group_by(Sala.id, Sala.nombre).all()
        
        # Tendencia de reservas
        reservas_por_dia = self.db.query(
            func.date(Reserva.fecha_inicio).label('fecha'),
            func.count(Reserva.id).label('cantidad')
        ).filter(
            Reserva.fecha_inicio >= start_date,
            Reserva.fecha_inicio <= end_date
        ).group_by(func.date(Reserva.fecha_inicio)).all()
        
        # Top usuarios
        top_usuarios = self.db.query(
            Persona.nombre,
            Persona.email,
            func.count(Reserva.id).label('total_reservas')
        ).join(Reserva).filter(
            Reserva.fecha_inicio >= start_date,
            Reserva.fecha_inicio <= end_date
        ).group_by(Persona.id).order_by(
            func.count(Reserva.id).desc()
        ).limit(5).all()
        
        return {
            'ocupacion_salas': [
                {
                    'sala': sala.nombre,
                    'reservas': sala.total_reservas or 0,
                    'horas_promedio': float(sala.horas_promedio or 0)
                } for sala in ocupacion_salas
            ],
            'tendencia_reservas': [
                {
                    'fecha': reserva.fecha.strftime('%Y-%m-%d'),
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
        # Patrón por día de la semana
        patron_semanal = self.db.query(
            func.extract('dow', Reserva.fecha_inicio).label('dia_semana'),
            func.avg(func.count(Reserva.id)).label('promedio_reservas')
        ).group_by(
            func.extract('dow', Reserva.fecha_inicio)
        ).subquery()
        
        # Generar predicciones
        predicciones = []
        today = datetime.utcnow().date()
        
        for i in range(dias_adelante):
            fecha_pred = today + timedelta(days=i)
            dia_semana = fecha_pred.weekday()
            
            # Buscar patrón histórico
            patron = self.db.query(patron_semanal).filter(
                patron_semanal.c.dia_semana == dia_semana
            ).first()
            
            predicciones.append({
                'fecha': fecha_pred.strftime('%Y-%m-%d'),
                'prediccion_reservas': int(patron.promedio_reservas) if patron else 0,
                'confianza': 0.75  # Simplificado, se puede mejorar
            })
            
        return {'predicciones': predicciones}
    
    def get_metricas_inventario(self) -> Dict:
        """Métricas de inventario y artículos"""
        # Artículos más utilizados
        articulos_populares = self.db.query(
            Articulo.nombre,
            Articulo.stock,
            func.count('*').label('uso_frecuencia')
        ).group_by(Articulo.id).order_by(
            func.count('*').desc()
        ).limit(10).all()
        
        # Stock bajo
        stock_critico = self.db.query(Articulo).filter(
            Articulo.stock < 5
        ).all()
        
        return {
            'articulos_populares': [
                {
                    'nombre': art.nombre,
                    'stock': art.stock,
                    'frecuencia': art.uso_frecuencia
                } for art in articulos_populares
            ],
            'stock_critico': [
                {
                    'nombre': art.nombre,
                    'stock': art.stock,
                    'id': art.id
                } for art in stock_critico
            ]
        }
