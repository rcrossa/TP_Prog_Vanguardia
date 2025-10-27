"""
Rutas web para la interfaz de usuario.

Este módulo define las rutas para servir las páginas HTML
del sistema de reservas.
"""

import os
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.auth.jwt_handler import extract_email_from_token
from app.core.database import get_db
from app.models.persona import Persona
from app.repositories.persona_repository import PersonaRepository
from app.services import PersonaService
from app.repositories.reserva_repository import ReservaRepository
from app.repositories.sala_repository import SalaRepository
from app.models.articulo import Articulo
from app.models.reserva import Reserva
from app.models.sala import Sala

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def handle_auth_error(request: Request):
    """Manejar errores de autenticación redirigiendo al login."""
    # Si es una petición AJAX, devolver JSON error
    if (
        request.headers.get("X-Requested-With") == "XMLHttpRequest"
        or request.headers.get("Content-Type") == "application/json"
    ):
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
    if not user:
        return handle_auth_error(request)
    if not user.is_admin:
        # Redirigir a reservas si el usuario está autenticado pero no es admin
        return RedirectResponse(url="/reservas", status_code=302)
    return None


@router.get("/debug-auth", response_class=HTMLResponse)
async def debug_auth(request: Request):
    """Página de debug para autenticación"""
    with open("static/test-auth.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """Dashboard principal (solo administradores)"""
    # Verificar autenticación
    current_user = get_user_from_request(request, db)
    if not current_user:
        return handle_auth_error(request)
    # Verificar permisos de admin
    admin_check = require_admin_access(current_user, request)
    if admin_check:
        return admin_check

    try:
        # Obtener estadísticas básicas para el dashboard


        personas = PersonaRepository.get_all(db)
        salas = SalaRepository.get_all(db)
        reservas = ReservaRepository.get_all(db)

        stats = {
            "total_personas": len(personas),
            "total_articulos": 0,  # Gestión de artículos movida al servicio Java
            "articulos_disponibles": 0,
            "articulos_no_disponibles": 0,
            "total_salas": len(salas),
            "salas_pequenas": len([s for s in salas if s.capacidad <= 20]),
            "salas_grandes": len([s for s in salas if s.capacidad > 20]),
            "total_reservas": len(reservas),
        }

        return templates.TemplateResponse(
            "dashboard.html", {"request": request, "stats": stats, "user": current_user}
        )
    except Exception as e:
        # En caso de error, devolver un dashboard básico
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "stats": {
                    "total_personas": 0,
                    "total_articulos": 0,
                    "articulos_disponibles": 0,
                    "articulos_no_disponibles": 0,
                    "total_salas": 0,
                    "salas_pequenas": 0,
                    "salas_grandes": 0,
                    "total_reservas": 0,
                },
                "user": current_user,
                "error": f"Error al cargar estadísticas: {str(e)}",
            },
        )


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
        {"request": request, "personas": personas, "user": current_user},
    )


@router.get("/salas", response_class=HTMLResponse)
async def salas_page(request: Request, db: Session = Depends(get_db)):
    """Página de gestión de salas."""
    # Verificar autenticación
    current_user = get_user_from_request(request, db)
    if not current_user:
        return handle_auth_error(request)

    return templates.TemplateResponse(
        "salas.html", {"request": request, "user": current_user}
    )


@router.get("/reservas", response_class=HTMLResponse)
async def reservas_page(request: Request, db: Session = Depends(get_db)):
    """Página de gestión de reservas."""
    # Verificar autenticación
    current_user = get_user_from_request(request, db)
    if not current_user:
        return handle_auth_error(request)

    return templates.TemplateResponse(
        "reservas.html", {"request": request, "user": current_user}
    )


@router.get("/inventario", response_class=HTMLResponse)
async def inventario_page(request: Request, db: Session = Depends(get_db)):
    """Página de gestión de inventario (solo administradores)."""
    # Verificar autenticación
    current_user = get_user_from_request(request, db)
    if not current_user:
        return handle_auth_error(request)

    # Verificar permisos de admin
    admin_check = require_admin_access(current_user, request)
    if admin_check:
        return admin_check

    return templates.TemplateResponse(
        "inventario.html", {"request": request, "user": current_user}
    )


@router.get("/reportes", response_class=HTMLResponse)
async def reportes_page(request: Request, db: Session = Depends(get_db)):
    """Página de reportes y analytics (solo administradores)."""
    # Verificar autenticación
    current_user = get_user_from_request(request, db)
    if not current_user:
        return handle_auth_error(request)

    # Verificar permisos de admin
    admin_check = require_admin_access(current_user, request)
    if admin_check:
        return admin_check

    return templates.TemplateResponse(
        "reportes.html", {"request": request, "user": current_user}
    )


@router.get("/configuracion", response_class=HTMLResponse)
async def configuracion_page(request: Request, db: Session = Depends(get_db)):
    """Página de configuración del sistema (solo administradores)."""
    # Verificar autenticación
    current_user = get_user_from_request(request, db)
    if not current_user:
        return handle_auth_error(request)

    # Verificar permisos de admin
    admin_check = require_admin_access(current_user, request)
    if admin_check:
        return admin_check

    # Leer contenido del README para la pestaña de documentación
    readme_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "README.md"
    )
    readme_content = ""
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
    except Exception as e:
        print(f"Error leyendo README: {e}")

    # Obtener estadísticas del sistema


    stats = {
        "total_usuarios": db.query(Persona).count(),
        "total_reservas": db.query(Reserva).count(),
        "total_salas": db.query(Sala).count(),
        "total_articulos": db.query(Articulo).count(),
    }

    return templates.TemplateResponse(
        "configuracion.html",
        {
            "request": request,
            "user": current_user,
            "readme_content": readme_content,
            "stats": stats,
        },
    )


@router.get("/documentacion", response_class=HTMLResponse)
async def documentacion_page(request: Request, db: Session = Depends(get_db)):
    """Página de documentación del proyecto (solo administradores)."""
    # Verificar autenticación
    current_user = get_user_from_request(request, db)
    if not current_user:
        return handle_auth_error(request)

    # Verificar permisos de admin
    admin_check = require_admin_access(current_user, request)
    if admin_check:
        return admin_check

    # Leer contenido del README para el mapa mental

    readme_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "README.md"
    )
    readme_content = ""
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
    except Exception as e:
        print(f"Error leyendo README: {e}")
        readme_content = "# Error\nNo se pudo cargar la documentación."

    return templates.TemplateResponse(
        "documentacion.html",
        {
            "request": request,
            "user": current_user,
            "readme_content": readme_content,
        },
    )


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Página de inicio de sesión."""
    return templates.TemplateResponse("login.html", {"request": request})
