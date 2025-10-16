"""
Rutas web para la interfaz de usuario.

Este módulo define las rutas para servir las páginas HTML
del sistema de reservas.
"""

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import PersonaService, SalaService, ReservaService
from app.auth.dependencies import get_current_admin_user, get_current_user
from app.auth.jwt_handler import verify_token, extract_email_from_token
from app.repositories.persona_repository import PersonaRepository
from app.models.persona import Persona

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def handle_auth_error(request: Request):
    """Manejar errores de autenticación redirigiendo al login."""
    # Si es una petición AJAX, devolver JSON error
    if request.headers.get("X-Requested-With") == "XMLHttpRequest" or \
       request.headers.get("Content-Type") == "application/json":
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Si es una petición web normal, redirigir al login
    return RedirectResponse(url="/login", status_code=302)


def get_user_from_request(request: Request, db: Session):
    """Extraer usuario desde el token en el header Authorization o cookies."""
    token = None
    
    # Intentar obtener token del header Authorization
    authorization = request.headers.get("Authorization")
    if authorization:
        try:
            scheme, token = authorization.split(" ", 1)
            if scheme.lower() != "bearer":
                token = None
        except ValueError:
            token = None
    
    # Si no hay token en el header, buscar en cookies
    if not token:
        token = request.cookies.get("token")
    
    # Si no hay token en ningún lado, intentar obtenerlo de localStorage (vía JavaScript)
    # Esto se manejará en el frontend
    if not token:
        return None
    
    try:
        email = extract_email_from_token(token)
        if not email:
            return None
        
        user = PersonaRepository.get_by_email(db, email)
        if not user or not user.is_active:
            return None
            
        return user
    except Exception:
        return None


def require_admin_access(user: Persona, request: Request):
    """Verificar que el usuario tenga permisos de admin."""
    if not user or not user.is_admin:
        return handle_auth_error(request)
    return None

@router.get("/debug-auth", response_class=HTMLResponse)
async def debug_auth(request: Request):
    """Página de debug para autenticación"""
    with open("static/test-auth.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """Dashboard principal"""
    try:
        # Obtener estadísticas básicas para el dashboard
        from app.repositories.persona_repository import PersonaRepository
        from app.repositories.sala_repository import SalaRepository  
        from app.repositories.reserva_repository import ReservaRepository
        
        personas = PersonaRepository.get_all(db)
        salas = SalaRepository.get_all(db) 
        reservas = ReservaRepository.get_all(db)
        
        stats = {
            'total_personas': len(personas),
            'total_articulos': 0,  # Gestión de artículos movida al servicio Java
            'articulos_disponibles': 0,
            'articulos_no_disponibles': 0,
            'total_salas': len(salas),
            'salas_pequenas': len([s for s in salas if s.capacidad <= 20]),
            'salas_grandes': len([s for s in salas if s.capacidad > 20]),
            'total_reservas': len(reservas),
        }
        
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "stats": stats
        })
    except Exception as e:
        # En caso de error, devolver un dashboard básico
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "stats": {
                'total_personas': 0,
                'total_articulos': 0,
                'articulos_disponibles': 0,
                'articulos_no_disponibles': 0,
                'total_salas': 0,
                'salas_pequenas': 0,
                'salas_grandes': 0,
                'total_reservas': 0,
            },
            "error": f"Error al cargar estadísticas: {str(e)}"
        })

@router.get("/personas", response_class=HTMLResponse)
async def personas_page(request: Request, db: Session = Depends(get_db)):
    """Página de gestión de personas (solo administradores)."""
    # Verificar autenticación
    current_user = get_user_from_request(request, db)
    if not current_user:
        return handle_auth_error(request)
    
    # Verificar permisos de admin
    admin_check = require_admin_access(current_user, request)
    if admin_check:
        return admin_check
    
    try:
        personas = PersonaService.get_personas(db, limit=50)
    except Exception as e:
        personas = []
    
    return templates.TemplateResponse(
        "personas.html", 
        {"request": request, "personas": personas, "user": current_user}
    )

@router.get("/salas", response_class=HTMLResponse)
async def salas_page(request: Request, db: Session = Depends(get_db)):
    """Página de gestión de salas."""
    return templates.TemplateResponse(
        "salas.html", 
        {"request": request}
    )

@router.get("/reservas", response_class=HTMLResponse)
async def reservas_page(request: Request, db: Session = Depends(get_db)):
    """Página de gestión de reservas."""
    return templates.TemplateResponse(
        "reservas.html", 
        {"request": request}
    )

@router.get("/inventario", response_class=HTMLResponse)
async def inventario_page(request: Request, db: Session = Depends(get_db)):
    """Página de gestión de inventario."""
    return templates.TemplateResponse(
        "inventario.html", 
        {"request": request}
    )

@router.get("/reportes", response_class=HTMLResponse)
async def reportes_page(request: Request, db: Session = Depends(get_db)):
    """Página de reportes y analytics."""
    return templates.TemplateResponse(
        "reportes.html", 
        {"request": request}
    )

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Página de inicio de sesión."""
    return templates.TemplateResponse(
        "login.html", 
        {"request": request}
    )