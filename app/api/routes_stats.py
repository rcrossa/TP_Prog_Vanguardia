from datetime import datetime, timedelta
import pytz
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.reserva_repository import ReservaRepository
from app.repositories.sala_repository import SalaRepository
from app.repositories.articulo_repository import ArticuloRepository
from app.repositories.persona_repository import PersonaRepository
from app.auth.jwt_handler import extract_email_from_token
from app.models.reserva import Reserva

router = APIRouter()

def get_authenticated_user(request: Request, db: Session):
    """Helper para obtener usuario autenticado desde token."""
    token = request.headers.get("Authorization")
    if token:
        try:
            scheme, token = token.split(" ", 1)
            if scheme.lower() != "bearer":
                token = None
        except ValueError:
            token = None
    if not token:
        token = request.cookies.get("token")
    if not token:
        return None

    email = extract_email_from_token(token)
    if not email:
        return None

    user = PersonaRepository.get_by_email(db, email)
    if not user or not user.is_active:
        return None

    return user


@router.get("/api/v1/stats/reservas", tags=["Stats"])
async def api_reservas_activas(request: Request, db: Session = Depends(get_db)):
    """DEPRECATED: Usar /api/v1/stats/reservas_activas en su lugar."""
    user = get_authenticated_user(request, db)
    if not user:
        return JSONResponse(status_code=401, content={"error": "No autorizado"})

    local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
    ahora_local = datetime.now(local_tz)
    reservas = ReservaRepository.get_all(db)
    reservas_activas = []
    for r in reservas:
        fin = r.fecha_hora_fin
        if fin.tzinfo is None:
            if fin >= ahora_local.replace(tzinfo=None):
                reservas_activas.append(r)
        else:
            if fin.astimezone(local_tz) >= ahora_local:
                reservas_activas.append(r)
    return {"reservasActivas": len(reservas_activas)}


@router.get("/api/v1/stats/reservas_activas", tags=["Stats"])
async def get_reservas_activas(request: Request, db: Session = Depends(get_db)):
    """Obtiene el número de reservas activas (futuras o en curso)."""
    user = get_authenticated_user(request, db)
    if not user:
        return JSONResponse(status_code=401, content={"error": "No autorizado"})

    local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
    ahora_local = datetime.now(local_tz)
    reservas = ReservaRepository.get_all(db)

    reservas_activas = []
    for r in reservas:
        fin = r.fecha_hora_fin
        if fin.tzinfo is None:
            if fin >= ahora_local.replace(tzinfo=None):
                reservas_activas.append(r)
        else:
            if fin.astimezone(local_tz) >= ahora_local:
                reservas_activas.append(r)

    return {"reservasActivas": len(reservas_activas)}


@router.get("/api/v1/stats/actividad_detallada", tags=["Stats"])
async def get_actividad_detallada(request: Request, db: Session = Depends(get_db)):
    """Obtiene reservas activas y pasadas por día (últimos 7 días)."""
    user = get_authenticated_user(request, db)
    if not user:
        return JSONResponse(status_code=401, content={"error": "No autorizado"})

    local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
    ahora_local = datetime.now(local_tz)

    # Últimos 7 días
    dias_labels = []
    activas_data = []
    pasadas_data = []

    for i in range(6, -1, -1):
        dia = ahora_local - timedelta(days=i)
        dia_inicio = dia.replace(hour=0, minute=0, second=0, microsecond=0)
        dia_fin = dia.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Formato de etiqueta: "Lun 1/11"
        dias_labels.append(dia.strftime("%a %d/%m"))

        # Contar reservas en este día
        reservas_dia = db.query(Reserva).filter(
            Reserva.fecha_hora_inicio >= dia_inicio.replace(tzinfo=None),
            Reserva.fecha_hora_inicio <= dia_fin.replace(tzinfo=None)
        ).all()

        activas = sum(1 for r in reservas_dia if r.fecha_hora_fin.replace(tzinfo=None) >= ahora_local.replace(tzinfo=None))
        pasadas = len(reservas_dia) - activas

        activas_data.append(activas)
        pasadas_data.append(pasadas)

    return {
        "dias": dias_labels,
        "activas": activas_data,
        "pasadas": pasadas_data
    }


@router.get("/api/v1/analytics/dashboard-metrics", tags=["Stats", "Analytics"])
async def get_dashboard_metrics(request: Request, days: int = 30, db: Session = Depends(get_db)):
    """Obtiene métricas consolidadas para el dashboard."""
    user = get_authenticated_user(request, db)
    if not user:
        return JSONResponse(status_code=401, content={"error": "No autorizado"})

    local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
    ahora_local = datetime.now(local_tz)
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
            "horas_promedio": horas_promedio
        })

    # 2. Tendencia de reservas (últimos días)
    tendencia_labels = []
    tendencia_values = []

    for i in range(min(days, 30), -1, -1):
        dia = ahora_local - timedelta(days=i)
        dia_inicio = dia.replace(hour=0, minute=0, second=0, microsecond=0)
        dia_fin = dia.replace(hour=23, minute=59, second=59, microsecond=999999)

        count = sum(
            1 for r in reservas
            if dia_inicio.replace(tzinfo=None) <= r.fecha_hora_inicio <= dia_fin.replace(tzinfo=None)
        )

        tendencia_labels.append(dia.strftime("%d/%m"))
        tendencia_values.append(count)

    # 3. Top usuarios (más reservas)
    from collections import Counter
    persona_counts = Counter(r.id_persona for r in reservas if r.id_persona)
    top_usuarios = []

    for persona_id, count in persona_counts.most_common(5):
        persona = PersonaRepository.get_by_id(db, persona_id)
        if persona:
            top_usuarios.append({
                "nombre": f"{persona.nombre} {persona.apellido or ''}".strip(),
                "reservas": count
            })

    # 4. Métricas generales
    reservas_hoy = sum(
        1 for r in reservas
        if r.fecha_hora_inicio.date() == ahora_local.date()
    )

    salas_disponibles = sum(1 for s in salas if s.disponible)

    articulos = ArticuloRepository.get_all(db)
    stock_critico = sum(1 for a in articulos if a.cantidad < 5 and a.disponible)

    # Calcular ocupación promedio
    if reservas:
        total_horas_reservadas = sum(
            (r.fecha_hora_fin - r.fecha_hora_inicio).total_seconds() / 3600
            for r in reservas
        )
        horas_disponibles = len(salas) * 24 * days
        ocupacion_promedio = (total_horas_reservadas / horas_disponibles * 100) if horas_disponibles > 0 else 0
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
            "salas_disponibles": salas_disponibles,
            "stock_critico": stock_critico
        }
    }

