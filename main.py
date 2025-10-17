"""
Aplicación principal del Sistema de Reservas.

Este módulo contiene la aplicación FastAPI principal con los endpoints
básicos y la configuración inicial del sistema de reservas.
"""

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.database import engine, Base, get_db
from app.core.config import settings
from app.api import api_router
from app.web import web_router
# Validar configuración crítica al inicio
try:
    settings.validate_required_settings()
    # Probar que se puede construir la URL de la base de datos
    db_url = settings.database_url
    print(f"✅ Configuración válida - Base de datos: {settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}")
except ValueError as e:
    print(f"❌ Error de configuración: {e}")
    print("💡 Tip: Copia .env.example a .env y configura las variables necesarias")
    raise

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

# Crear aplicación FastAPI
app = FastAPI(
    title="🏢 Sistema de Reservas API",
    description="""
    ## 📋 API Completa para Gestión de Reservas

    Esta API REST permite gestionar un sistema completo de reservas de salas y artículos.
    
    ### 🚀 Características Principales
    
    * **👥 Gestión de Personas** - CRUD completo con validación de emails únicos
    * **📦 Gestión de Artículos** - Control de disponibilidad y reservas
    * **🏢 Gestión de Salas** - Configuración de capacidad y horarios
    * **📅 Sistema de Reservas** - Reservas inteligentes con detección de conflictos
    
    ### 🔧 Funcionalidades Avanzadas
    
    * ✅ Validación automática de conflictos de horarios
    * ✅ Verificación de disponibilidad en tiempo real
    * ✅ Relaciones complejas entre entidades
    * ✅ Paginación y filtros inteligentes
    * ✅ Documentación interactiva completa
    
    ### 📊 Base de Datos
    
    Utiliza PostgreSQL con SQLAlchemy 2.0 para máximo rendimiento y confiabilidad.
    
    ### 🎯 Casos de Uso
    
    - **Oficinas corporativas**: Reserva de salas de reuniones
    - **Bibliotecas**: Reserva de libros y salas de estudio
    - **Universidades**: Gestión de aulas y equipos
    - **Espacios de coworking**: Reserva de escritorios y recursos
    
    ---
    
    **💡 Tip**: Usa la sección "Try it out" para probar los endpoints directamente.
    """,
    version="1.0.0",
    debug=settings.debug,
    contact={
        "name": "Equipo de Desarrollo",
        "url": "https://github.com/rcrossa/TP_Prog_Vanguardia",
        "email": "dev@sistemarreservas.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    terms_of_service="https://sistemarreservas.com/terms",
    openapi_tags=[
        {
            "name": "personas",
            "description": "👥 **Gestión de Personas** - Operaciones CRUD para usuarios del sistema. Incluye validación de emails únicos y gestión de información personal.",
        },
        {
            "name": "articulos", 
            "description": "📦 **Gestión de Artículos** - Control completo de artículos reservables. Manejo de disponibilidad, estados y operaciones CRUD.",
        },
        {
            "name": "salas",
            "description": "🏢 **Gestión de Salas** - Administración de espacios físicos. Configuración de capacidades y características de las salas.",
        },
        {
            "name": "reservas",
            "description": "📅 **Sistema de Reservas** - Motor inteligente de reservas con detección automática de conflictos. Soporta reservas de artículos y salas con validaciones temporales.",
        },
        {
            "name": " Sistema",
            "description": "🏠 **Información del Sistema** - Endpoints de sistema incluyendo health checks, estadísticas y información general de la API.",
        },
    ]
)

# Configurar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir routers
app.include_router(api_router, prefix="/api/v1")
app.include_router(web_router)

@app.get(
    "/stats",
    tags=["🏠 Sistema"],
    summary="📊 Estadísticas del Sistema",
    description="Resumen estadístico completo del estado actual del sistema",
    responses={
        200: {
            "description": "Estadísticas del sistema",
            "content": {
                "application/json": {
                    "example": {
                        "personas": {"total": 25, "activas": 23},
                        "articulos": {"total": 45, "disponibles": 38, "reservados": 7},
                        "salas": {"total": 12, "pequeñas": 6, "grandes": 6},
                        "reservas": {"total": 156, "activas": 23, "completadas": 133},
                        "timestamp": "2025-10-15T17:48:12.095000"
                    }
                }
            }
        }
    }
)
async def get_system_stats(db: Session = Depends(get_db)):
    """
    ## 📊 Dashboard de Estadísticas
    
    Proporciona un resumen ejecutivo del estado actual del sistema.
    
    ### 📈 Métricas Incluidas
    
    **👥 Personas**
    - Total de usuarios registrados
    - Usuarios activos (con reservas)
    
    **📦 Artículos**
    - Inventario total
    - Disponibles para reserva
    - Actualmente reservados
    
    **🏢 Salas**
    - Total de espacios
    - Distribución por capacidad
    
    **📅 Reservas**
    - Total histórico
    - Reservas activas actuales
    - Reservas completadas
    
    ### 🎯 Casos de Uso
    - Dashboards administrativos
    - Reportes ejecutivos
    - Monitoreo de utilización
    - Planificación de recursos
    """
    try:
        from app.services import PersonaService, ArticuloService, SalaService, ReservaService
        from datetime import datetime
        
        return {
            "personas": {
                "total": PersonaService.count_personas(db)
            },
            "articulos": {
                "total": ArticuloService.count_articulos(db),
                "disponibles": ArticuloService.count_articulos(db, disponible=True),
                "no_disponibles": ArticuloService.count_articulos(db, disponible=False)
            },
            "salas": {
                "total": SalaService.count_salas(db),
                "pequeñas": SalaService.count_salas(db, min_capacidad=1) - SalaService.count_salas(db, min_capacidad=21),
                "grandes": SalaService.count_salas(db, min_capacidad=21)
            },
            "reservas": {
                "total": ReservaService.count_reservas(db)
            },
            "sistema": {
                "version": "1.0.0",
                "estado": "🟢 Operativo",
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar estadísticas: {str(e)}"
        ) from e

@app.get(
    "/",
    tags=["🏠 Sistema"],
    summary="🏠 Información del Sistema",
    description="Endpoint de bienvenida con información básica de la API",
    responses={
        200: {
            "description": "Información del sistema",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Bienvenido al Sistema de Reservas API",
                        "version": "1.0.0",
                        "status": "🟢 Operativo",
                        "features": ["CRUD Personas", "CRUD Artículos", "CRUD Salas", "Sistema Reservas"],
                        "docs": "/docs",
                        "redoc": "/redoc"
                    }
                }
            }
        }
    }
)
async def root():
    """
    ## 🏠 Sistema de Reservas API
    
    Bienvenido a la API más completa para gestión de reservas.
    
    ### 🚀 Características Principales
    - **CRUD Completo** para todas las entidades
    - **Validaciones Inteligentes** automáticas
    - **Detección de Conflictos** en tiempo real
    - **Documentación Interactiva** con Swagger UI
    
    ### 📚 Documentación
    - **Swagger UI**: `/docs` (Interfaz interactiva)
    - **ReDoc**: `/redoc` (Documentación alternativa)
    
    ### 🏃‍♂️ Empezar Ahora
    1. Explora los endpoints en `/docs`
    2. Crea personas, artículos y salas
    3. Prueba el sistema de reservas inteligente
    """
    return {
        "message": "🏢 Bienvenido al Sistema de Reservas API",
        "version": "1.0.0",
        "status": "🟢 Operativo",
        "features": [
            "👥 CRUD Personas",
            "📦 CRUD Artículos", 
            "🏢 CRUD Salas",
            "📅 Sistema Reservas Inteligente"
        ],
        "endpoints": {
            "personas": "/api/v1/personas",
            "articulos": "/api/v1/articulos",
            "salas": "/api/v1/salas", 
            "reservas": "/api/v1/reservas"
        },
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }

@app.get(
    "/health",
    tags=["🏠 Sistema"],
    summary="🏥 Health Check",
    description="Verificación del estado de la aplicación y conectividad de base de datos",
    responses={
        200: {
            "description": "Sistema funcionando correctamente",
            "content": {
                "application/json": {
                    "example": {
                        "status": "🟢 healthy",
                        "database": "🟢 connected",
                        "timestamp": "2025-10-15T17:48:12.095000",
                        "version": "1.0.0",
                        "message": "La aplicación y base de datos están funcionando correctamente"
                    }
                }
            }
        },
        503: {
            "description": "Servicio no disponible - Error de base de datos",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error de conexión a la base de datos: connection refused"
                    }
                }
            }
        }
    }
)
async def health_check(db: Session = Depends(get_db)):
    """
    ## 🏥 Health Check del Sistema
    
    Verifica el estado general de la aplicación y sus dependencias.
    
    ### ✅ Verificaciones Realizadas
    - **🔗 Conectividad**: Estado de conexión a PostgreSQL
    - **⚡ Responsividad**: Tiempo de respuesta de la base de datos
    - **🏃 Aplicación**: Estado general del servidor FastAPI
    
    ### 📊 Estados Posibles
    - **🟢 Healthy**: Todo funcionando correctamente
    - **🔴 Unhealthy**: Error de conexión o servicio caído
    
    ### 🚨 Uso en Producción
    Este endpoint es ideal para:
    - Monitoreo automatizado (Kubernetes health checks)
    - Balanceadores de carga (health probes)
    - Sistemas de alerta y observabilidad
    """
    try:
        from datetime import datetime
        # Verificar conexión a la base de datos
        db.execute(text("SELECT 1"))
        return {
            "status": "🟢 healthy",
            "database": "🟢 connected", 
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "components": {
                "fastapi": "🟢 running",
                "postgresql": "🟢 connected",
                "sqlalchemy": "🟢 active"
            },
            "message": "La aplicación y base de datos están funcionando correctamente"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"🔴 Error de conexión a la base de datos: {str(e)}"
        ) from e

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
        )