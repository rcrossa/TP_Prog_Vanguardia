"""
Aplicación principal del Sistema de Reservas.

Este módulo contiene la aplicación FastAPI principal con los endpoints
básicos y la configuración inicial del sistema de reservas.
"""

import os
from datetime import datetime
import uvicorn
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.core.config import settings
from app.core.database import Base, engine, get_db
from app.web import web_router
from app.services import (
    ArticuloService,
    PersonaService,
    ReservaService,
    SalaService,
)
from app.api.v1.endpoints import stats

# Crear aplicación FastAPI
app = FastAPI(
    # ...existing code...
)

# Handler global para errores inesperados
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Manejador global de excepciones."""
    _ = request  # Unused argument
    return JSONResponse(
        status_code=500,
        content={"detail": f"Error inesperado: {str(exc)}"}
    )
# Validar configuración crítica al inicio
try:
    settings.validate_required_settings()
    # Probar que se puede construir la URL de la base de datos
    db_url = settings.database_url
    print(
        f"✅ Configuración válida - Base de datos: "
        f"{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
    )
except ValueError as e:
    print(f"❌ Error de configuración: {e}")
    print("💡 Tip: Copia .env.example a .env y configura las variables necesarias")
    raise

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

# Crear aplicación FastAPI
app = FastAPI(
    title="Sistema de Reservas API",
    description="API REST para gestión de reservas de salas y artículos con detección de conflictos y validación automática.",
    version="1.0.0",
    debug=settings.debug,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir routers
app.include_router(api_router, prefix="/api/v1")
app.include_router(web_router)


@app.get(
    "/stats",
    tags=["Sistema"],
    summary="Estadísticas del Sistema",
)
async def get_system_stats(db: Session = Depends(get_db)):
    """Obtener resumen estadístico del sistema."""
    try:
        return {
            "personas": {"total": PersonaService.count_personas(db)},
            "articulos": {
                "total": ArticuloService.count_articulos(db),
                "disponibles": ArticuloService.count_articulos(db, disponible=True),
                "no_disponibles": ArticuloService.count_articulos(db, disponible=False),
            },
            "salas": {
                # Asumiendo que count_salas no recibe db, solo min_capacidad
                "total": SalaService.count_salas(),
                "pequeñas": SalaService.count_salas(min_capacidad=1),
                "grandes": SalaService.count_salas(min_capacidad=21),
            },
            "reservas": {"total": ReservaService.count_reservas(db)},
            "sistema": {
                "version": "1.0.0",
                "estado": "operativo",
                "timestamp": datetime.now().isoformat(),
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar estadísticas: {str(e)}",
        ) from e


@app.get(
    "/",
    tags=["Sistema"],
    summary="Información del Sistema",
)
async def root():
    """Endpoint raíz con información básica de la API."""
    return {
        "message": "Sistema de Reservas API",
        "version": "1.0.0",
        "status": "operativo",
        "docs": "/docs",
        "health": "/health",
    }


@app.get(
    "/health",
    tags=["Sistema"],
    summary="Health Check",
)
async def health_check(db: Session = Depends(get_db)):
    """Verificar estado del sistema y conectividad de base de datos."""
    try:
        # Verificar conexión a la base de datos
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error de conexión a la base de datos: {str(e)}",
        ) from e


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.debug)
