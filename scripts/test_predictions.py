#!/usr/bin/env python3
"""
Script de prueba para el módulo de predicciones.

Este script prueba todos los endpoints de predicción y verifica
que estén funcionando correctamente.
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import get_db
from app.prediction.prediction_service import PredictionService


def main():
    """Función principal de pruebas."""
    print("=" * 80)
    print("🧪 PRUEBA DEL MÓDULO DE PREDICCIONES")
    print("=" * 80)
    print()

    # Obtener sesión de base de datos
    db = next(get_db())

    try:
        # Crear instancia del servicio
        prediction_service = PredictionService(db)

        # ===== PRUEBA 1: Predicción de Demanda Semanal =====
        print("📊 PRUEBA 1: Predicción de Demanda Semanal")
        print("-" * 80)
        result = prediction_service.predict_weekly_demand(dias_adelante=7)

        print(f"✅ Predicciones generadas: {len(result['predicciones'])}")
        print(
            f"📈 Total reservas históricas: "
            f"{result['metadata']['total_reservas_historicas']}"
        )
        print(f"📉 Tendencia: {result['metadata']['tendencia']}")
        print(f"📊 Factor tendencia: {result['metadata']['factor_tendencia']:.3f}")
        print()

        print("Predicciones detalladas:")
        for pred in result["predicciones"]:
            emoji = {
                "muy_alta": "🔴",
                "alta": "🟡",
                "media": "🟢",
                "baja": "🔵",
                "muy_baja": "⚫",
            }.get(pred["nivel_demanda"], "⚪")

            print(
                f"  {emoji} {pred['dia_semana']} {pred['fecha']}: "
                f"{pred['prediccion_reservas']:2d} reservas "
                f"(confianza: {pred['confianza']*100:5.1f}%)"
            )
        print()

        # ===== PRUEBA 2: Horarios Pico =====
        print("📊 PRUEBA 2: Horarios Pico")
        print("-" * 80)
        result = prediction_service.predict_peak_hours(dias_analizar=30)

        print(f"✅ Periodo analizado: {result['periodo_analizado']}")
        print()

        for dia, horarios in result["horarios_pico"].items():
            if horarios:
                print(f"  {dia}:")
                for hora in horarios[:3]:  # Top 3
                    print(
                        f"    └─ {hora['hora']}: {hora['reservas']} reservas "
                        f"({hora['porcentaje']:.1f}%)"
                    )
            else:
                print(f"  {dia}: Sin datos")
        print()

        # ===== PRUEBA 3: Detección de Anomalías =====
        print("📊 PRUEBA 3: Detección de Anomalías")
        print("-" * 80)
        result = prediction_service.detect_anomalies(dias_analizar=30)

        stats = result["estadisticas"]
        print(f"✅ Promedio diario: {stats['promedio_diario']:.1f} reservas")
        print(f"📊 Desviación estándar: {stats['desviacion_estandar']:.1f}")
        print(f"⬆️  Umbral alto: {stats['umbral_alto']:.1f}")
        print(f"⬇️  Umbral bajo: {stats['umbral_bajo']:.1f}")
        print(f"🚨 Total anomalías: {stats['total_anomalias']}")
        print()

        if result["anomalias"]:
            print("Anomalías detectadas:")
            for anomalia in result["anomalias"][:5]:  # Mostrar max 5
                emoji = "🔴" if anomalia["tipo"] == "alta" else "🔵"
                print(
                    f"  {emoji} {anomalia['fecha']}: {anomalia['reservas']} reservas "
                    f"(diferencia: {anomalia['diferencia_promedio']:+.1f}, "
                    f"severidad: {anomalia['severidad']})"
                )
        else:
            print("  ℹ️  No se detectaron anomalías")
        print()

        # ===== PRUEBA 4: Recomendaciones de Capacidad =====
        print("📊 PRUEBA 4: Recomendaciones de Capacidad")
        print("-" * 80)
        result = prediction_service.recommend_capacity(dias_adelante=7)

        print(f"✅ Capacidad total: {result['capacidad_total']} salas")
        print()

        print("Recomendaciones por día:")
        for rec in result["recomendaciones"]:
            estado_emoji = {
                "bajo": "🟢",
                "moderado": "🟡",
                "alto": "🟠",
                "crítico": "🔴",
            }.get(rec["estado"], "⚪")

            print(
                f"  {estado_emoji} {rec['dia_semana']} {rec['fecha']}: "
                f"{rec['salas_recomendadas']} salas "
                f"({rec['utilizacion_esperada']:.1f}% utilización)"
            )
            print(f"     └─ {rec['accion']}")
        print()

        # ===== RESUMEN FINAL =====
        print("=" * 80)
        print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("=" * 80)
        print()
        print("📝 Resumen:")
        print("  • Predicción de demanda: ✅ Funcional")
        print("  • Horarios pico: ✅ Funcional")
        print("  • Detección de anomalías: ✅ Funcional")
        print("  • Recomendaciones de capacidad: ✅ Funcional")
        print()
        print("🎉 El módulo de predicciones está listo para usar!")
        print()

        return 0

    except Exception as e:  # noqa: BLE001
        print(f"❌ ERROR: {str(e)}")
        import traceback

        traceback.print_exc()
        return 1

    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
