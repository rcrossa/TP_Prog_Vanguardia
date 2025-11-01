"""
Servicio de predicciones para el sistema de reservas.

Este módulo implementa predicciones basadas en patrones históricos
usando técnicas de análisis de series temporales simples.
"""
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.reserva import Reserva
from app.models.sala import Sala


class PredictionService:
    """Servicio para predicciones de ocupación y demanda."""

    def __init__(self, db: Session):
        self.db = db

    def predict_weekly_demand(self, dias_adelante: int = 7) -> Dict:
        """
        Predice la demanda de reservas para los próximos días.

        Utiliza:
        - Patrones por día de la semana
        - Tendencia mensual
        - Promedio móvil de los últimos 30 días

        Args:
            dias_adelante: Número de días a predecir (1-30)

        Returns:
            Dict con predicciones detalladas por día
        """
        # 1. Obtener datos históricos (últimos 60 días)
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=60)

        reservas_historicas = self.db.query(Reserva).filter(
            Reserva.fecha_hora_inicio >= start_date,
            Reserva.fecha_hora_inicio <= end_date
        ).all()

        # 2. Calcular patrones por día de semana
        patron_semanal = self._calculate_weekly_pattern(reservas_historicas)

        # 3. Calcular tendencia
        tendencia = self._calculate_trend(reservas_historicas)

        # 4. Generar predicciones
        predicciones = []
        today = datetime.utcnow().date()

        for i in range(1, dias_adelante + 1):
            fecha_pred = today + timedelta(days=i)
            dia_semana = fecha_pred.weekday()

            # Obtener predicción base del patrón semanal
            prediccion_base = patron_semanal.get(dia_semana, 0)

            # Ajustar por tendencia
            factor_tendencia = 1 + (tendencia * i / 30)  # Ajuste gradual
            prediccion_ajustada = int(prediccion_base * factor_tendencia)

            # Calcular nivel de confianza
            confianza = self._calculate_confidence(
                patron_semanal,
                dia_semana,
                len(reservas_historicas)
            )

            # Determinar nivel de demanda
            nivel_demanda = self._classify_demand_level(prediccion_ajustada)

            predicciones.append({
                'fecha': fecha_pred.strftime('%Y-%m-%d'),
                'dia_semana': ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'][dia_semana],
                'prediccion_reservas': prediccion_ajustada,
                'confianza': round(confianza, 2),
                'nivel_demanda': nivel_demanda,
                'recomendacion': self._generate_recommendation(
                    prediccion_ajustada,
                    nivel_demanda
                )
            })

        return {
            'predicciones': predicciones,
            'metadata': {
                'dias_historicos': 60,
                'total_reservas_historicas': len(reservas_historicas),
                'tendencia': 'creciente' if tendencia > 0 else 'decreciente',
                'factor_tendencia': round(tendencia, 3)
            }
        }

    def predict_peak_hours(self, dias_analizar: int = 30) -> Dict:
        """
        Identifica los horarios pico de reservas.

        Args:
            dias_analizar: Días históricos a analizar

        Returns:
            Dict con horarios pico por día de semana
        """
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=dias_analizar)

        reservas = self.db.query(Reserva).filter(
            Reserva.fecha_hora_inicio >= start_date,
            Reserva.fecha_hora_inicio <= end_date
        ).all()

        # Agrupar por día de semana y hora
        horarios = defaultdict(lambda: defaultdict(int))

        for reserva in reservas:
            dia_semana = reserva.fecha_hora_inicio.weekday()
            hora = reserva.fecha_hora_inicio.hour
            horarios[dia_semana][hora] += 1

        # Identificar horas pico por día
        picos_por_dia = {}
        dias_nombres = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

        for dia in range(7):
            horas_dia = horarios.get(dia, {})
            if horas_dia:
                # Top 3 horas más ocupadas
                top_horas = sorted(
                    horas_dia.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:3]

                picos_por_dia[dias_nombres[dia]] = [
                    {
                        'hora': f"{hora:02d}:00",
                        'reservas': count,
                        'porcentaje': round(
                            count / sum(horas_dia.values()) * 100, 1
                        )
                    } for hora, count in top_horas
                ]
            else:
                picos_por_dia[dias_nombres[dia]] = []

        return {
            'horarios_pico': picos_por_dia,
            'periodo_analizado': f'{dias_analizar} días'
        }

    def detect_anomalies(self, dias_analizar: int = 30) -> Dict:
        """
        Detecta días con ocupación anormal (muy alta o muy baja).

        Args:
            dias_analizar: Días a analizar

        Returns:
            Dict con anomalías detectadas
        """
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=dias_analizar)

        # Contar reservas por día
        reservas_por_dia = self.db.query(
            func.date(Reserva.fecha_hora_inicio).label('fecha'),
            func.count(Reserva.id).label('cantidad')  # type: ignore
        ).filter(
            Reserva.fecha_hora_inicio >= start_date,
            Reserva.fecha_hora_inicio <= end_date
        ).group_by(func.date(Reserva.fecha_hora_inicio)).all()

        if not reservas_por_dia:
            return {'anomalias': [], 'estadisticas': {}}

        # Calcular estadísticas
        cantidades = [r.cantidad for r in reservas_por_dia]
        promedio = sum(cantidades) / len(cantidades)
        desviacion = (
            sum((x - promedio) ** 2 for x in cantidades) / len(cantidades)
        ) ** 0.5

        # Detectar anomalías (±2 desviaciones estándar)
        anomalias = []
        umbral_alto = promedio + (2 * desviacion)
        umbral_bajo = max(0, promedio - (2 * desviacion))

        for reserva in reservas_por_dia:
            if reserva.cantidad > umbral_alto:
                anomalias.append({
                    'fecha': reserva.fecha.strftime('%Y-%m-%d'),
                    'tipo': 'alta',
                    'reservas': reserva.cantidad,
                    'diferencia_promedio': round(reserva.cantidad - promedio, 1),
                    'severidad': 'alta' if reserva.cantidad > umbral_alto * 1.5 else 'media'
                })
            elif reserva.cantidad < umbral_bajo:
                anomalias.append({
                    'fecha': reserva.fecha.strftime('%Y-%m-%d'),
                    'tipo': 'baja',
                    'reservas': reserva.cantidad,
                    'diferencia_promedio': round(reserva.cantidad - promedio, 1),
                    'severidad': 'media'
                })

        return {
            'anomalias': sorted(anomalias, key=lambda x: x['fecha'], reverse=True),
            'estadisticas': {
                'promedio_diario': round(promedio, 1),
                'desviacion_estandar': round(desviacion, 1),
                'umbral_alto': round(umbral_alto, 1),
                'umbral_bajo': round(umbral_bajo, 1),
                'total_anomalias': len(anomalias)
            }
        }

    def recommend_capacity(self, dias_adelante: int = 7) -> Dict:
        """
        Recomienda capacidad de salas necesaria basada en predicciones.

        Args:
            dias_adelante: Días a analizar

        Returns:
            Dict con recomendaciones de capacidad
        """
        # Obtener predicciones
        predicciones = self.predict_weekly_demand(dias_adelante)

        # Obtener total de salas
        total_salas = self.db.query(func.count(Sala.id)).scalar() or 1  # type: ignore

        # Calcular ocupación esperada por día
        recomendaciones = []

        for pred in predicciones['predicciones']:
            reservas_pred = pred['prediccion_reservas']

            # Asumir promedio de 2 horas por reserva
            salas_necesarias = min(
                int(reservas_pred / 4) + 1,  # 4 reservas por sala/día
                total_salas
            )

            nivel_utilizacion = (salas_necesarias / total_salas) * 100

            recomendaciones.append({
                'fecha': pred['fecha'],
                'dia_semana': pred['dia_semana'],
                'salas_recomendadas': salas_necesarias,
                'utilizacion_esperada': round(nivel_utilizacion, 1),
                'estado': self._classify_capacity_status(nivel_utilizacion),
                'accion': self._suggest_capacity_action(nivel_utilizacion)
            })

        return {
            'recomendaciones': recomendaciones,
            'capacidad_total': total_salas
        }

    # --- Métodos privados auxiliares ---

    def _calculate_weekly_pattern(self, reservas: List[Reserva]) -> Dict[int, float]:
        """Calcula el promedio de reservas por día de la semana."""
        patron = defaultdict(list)

        for reserva in reservas:
            dia_semana = reserva.fecha_hora_inicio.weekday()
            patron[dia_semana].append(1)

        # Calcular promedio
        return {
            dia: sum(counts) / len(counts) if counts else 0
            for dia, counts in patron.items()
        }

    def _calculate_trend(self, reservas: List[Reserva]) -> float:
        """Calcula la tendencia de crecimiento/decrecimiento."""
        if len(reservas) < 2:
            return 0.0

        # Dividir en dos mitades
        mitad = len(reservas) // 2
        primera_mitad = reservas[:mitad]
        segunda_mitad = reservas[mitad:]

        avg_primera = len(primera_mitad) / 30 if primera_mitad else 0
        avg_segunda = len(segunda_mitad) / 30 if segunda_mitad else 0

        # Calcular cambio porcentual
        if avg_primera > 0:
            return (avg_segunda - avg_primera) / avg_primera
        return 0.0

    def _calculate_confidence(
        self,
        patron: Dict[int, float],
        dia_semana: int,
        total_datos: int
    ) -> float:
        """Calcula el nivel de confianza de la predicción."""
        # Confianza base según cantidad de datos
        confianza_base = min(0.5 + (total_datos / 200), 0.95)

        # Reducir confianza si no hay datos para ese día
        if patron.get(dia_semana, 0) == 0:
            confianza_base *= 0.5

        return confianza_base

    def _classify_demand_level(self, prediccion: int) -> str:
        """Clasifica el nivel de demanda."""
        if prediccion >= 20:
            return 'muy_alta'
        elif prediccion >= 15:
            return 'alta'
        elif prediccion >= 10:
            return 'media'
        elif prediccion >= 5:
            return 'baja'
        else:
            return 'muy_baja'

    def _generate_recommendation(self, prediccion: int, nivel: str) -> str:
        """Genera recomendación basada en predicción."""
        if nivel == 'muy_alta':
            return f'⚠️ Demanda muy alta esperada ({prediccion} reservas). Preparar todas las salas.'
        elif nivel == 'alta':
            return f'📈 Demanda alta ({prediccion} reservas). Verificar disponibilidad.'
        elif nivel == 'media':
            return f'✅ Demanda normal ({prediccion} reservas).'
        elif nivel == 'baja':
            return f'📉 Demanda baja ({prediccion} reservas). Considerar mantenimiento.'
        else:
            return f'ℹ️ Demanda muy baja ({prediccion} reservas).'

    def _classify_capacity_status(self, utilizacion: float) -> str:
        """Clasifica el estado de capacidad."""
        if utilizacion >= 90:
            return 'crítico'
        elif utilizacion >= 75:
            return 'alto'
        elif utilizacion >= 50:
            return 'moderado'
        else:
            return 'bajo'

    def _suggest_capacity_action(self, utilizacion: float) -> str:
        """Sugiere acción basada en utilización."""
        if utilizacion >= 90:
            return 'Considerar habilitar salas adicionales'
        elif utilizacion >= 75:
            return 'Monitorear disponibilidad de cerca'
        elif utilizacion >= 50:
            return 'Capacidad adecuada'
        else:
            return 'Exceso de capacidad disponible'
