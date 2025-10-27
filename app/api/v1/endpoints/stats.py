"""Stats endpoints for the API."""

from collections import Counter
from datetime import datetime, timedelta
import pytz
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.auth.dependencies import get_current_admin_user
from app.models.reserva import Reserva
from app.models.sala import Sala
from app.models.articulo import Articulo
from app.models.persona import Persona

router = APIRouter(prefix="/stats", tags=["stats"])

# Nuevo endpoint para actividad detallada (dashboard)
@router.get("/actividad_detallada")
def stats_actividad_detallada(
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_admin_user)
):
    """Reservas activas y pasadas por día en los últimos 7 días."""
    hoy = datetime.now().date()
    reservas = db.query(Reserva).all()
    dias = [(hoy - timedelta(days=i)) for i in range(6, -1, -1)]
    activas = []
    pasadas = []
    for d in dias:
        activas_dia = 0
        pasadas_dia = 0
        for r in reservas:
            # Reserva activa: está en curso en ese día
            if r.fecha_hora_inicio.date() <= d <= r.fecha_hora_fin.date():
                activas_dia += 1
            # Reserva pasada: terminó antes de ese día
            elif r.fecha_hora_fin.date() < d:
                pasadas_dia += 1
        activas.append(activas_dia)
        pasadas.append(pasadas_dia)
    return {
        "dias": [str(d) for d in dias],
        "activas": activas,
        "pasadas": pasadas
    }
@router.get("/actividad")
def stats_actividad(
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_admin_user)
):
    """Reservas por día en los últimos 7 días."""
    hoy = datetime.now().date()
    reservas = db.query(Reserva).all()
    dias = [(hoy - timedelta(days=i)) for i in range(6, -1, -1)]
    actividad = {str(d): 0 for d in dias}
    for r in reservas:
        dia = r.fecha_hora_inicio.date()
        if dia in actividad:
            actividad[str(dia)] += 1
    return {"actividad": actividad}

@router.get("/reservas")
def stats_reservas(
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_admin_user)
):
    """Estadísticas de reservas."""
    reservas = db.query(Reserva).all()
    now = datetime.now()
    total = len(reservas)
    reservas_activas = len([
        r for r in reservas if r.fecha_hora_inicio <= now and r.fecha_hora_fin >= now
    ])
    reservas_futuras = len([
        r for r in reservas if r.fecha_hora_inicio > now
    ])
    # Salas más populares
    sala_ids = [r.sala_id for r in reservas if r.sala_id is not None]
    sala_counter = Counter(sala_ids)
    sala_counts = sala_counter.most_common(3)
    salas_populares = [f"Sala {sid}" for sid, _ in sala_counts if sid]

    # Total salas activas y futuras usando Python puro
    salas_activas = len(
        set(
            r.sala_id
            for r in reservas
            if r.fecha_hora_inicio <= now
            and r.fecha_hora_fin >= now
            and r.sala_id is not None
        )
    )
    salas_futuras = len(
        set(
            r.sala_id
            for r in reservas
            if r.fecha_hora_inicio > now and r.sala_id is not None
        )
    )
    # Artículos más populares
    articulo_ids = [r.articulo_id for r in reservas if r.articulo_id is not None]
    articulo_counter = Counter(articulo_ids)
    articulo_counts = articulo_counter.most_common(2)
    articulos_populares = [f"Artículo {aid}" for aid, _ in articulo_counts if aid]
    return {
        "totalReservas": total,
        "reservasActivas": reservas_activas,
        "reservasFuturas": reservas_futuras,
        "salasPopulares": salas_populares or ["Sin reservas de salas"],
        "articulosPopulares": articulos_populares or ["Sin reservas de artículos"],
        "salasActivas": salas_activas or 0,
        "salasFuturas": salas_futuras or 0,
    }

@router.get("/uso")
def stats_uso(
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_admin_user)
):
    """Estadísticas generales de uso del sistema."""
    total_usuarios = db.query(Persona).count()
    total_articulos = db.query(Articulo).count()
    total_salas = db.query(Sala).count()
    total_reservas = db.query(Reserva).count()
    hoy = datetime.now().date()
    reservas = db.query(Reserva).all()
    reservas_hoy = len(
        set(
            r.id_sala
            for r in reservas
            if r.fecha_hora_inicio.date() == hoy and r.id_sala is not None
        )
    )
    salas_libres = max(0, total_salas - reservas_hoy)
    disponibilidad_promedio = (
        int((salas_libres / total_salas) * 100) if total_salas > 0 else 0
    )
    return {
        "usuariosActivos": total_usuarios,
        "articulosReservados": total_reservas,
        "disponibilidadPromedio": disponibilidad_promedio,
        "totalSalas": total_salas,
        "totalArticulos": total_articulos,
    }

@router.get("/reservas_activas", tags=["stats"])
def reservas_activas_endpoint(db: Session = Depends(get_db)):
    """Devuelve el número de reservas activas (para dashboard)."""
    local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
    ahora_local = datetime.now(local_tz)
    reservas = db.query(Reserva).all()
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