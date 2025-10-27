from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import pytz
from datetime import datetime
from app.core.database import get_db
from app.repositories.reserva_repository import ReservaRepository
from app.auth.jwt_handler import extract_email_from_token
from app.repositories.persona_repository import PersonaRepository

router = APIRouter()

@router.get("/api/v1/stats/reservas", tags=["Stats"])
async def api_reservas_activas(request: Request, db: Session = Depends(get_db)):
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
        return JSONResponse(status_code=401, content={"error": "No autorizado"})
    email = extract_email_from_token(token)
    if not email:
        return JSONResponse(status_code=401, content={"error": "No autorizado"})
    user = PersonaRepository.get_by_email(db, email)
    if not user or not user.is_active:
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
