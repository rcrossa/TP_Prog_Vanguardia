"""
Configuración y conexión a la base de datos.

Este módulo configura la conexión a PostgreSQL usando SQLAlchemy
y proporciona la sesión de base de datos para toda la aplicación.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Base para los modelos
Base = declarative_base()

# Crear motor de base de datos usando configuración segura
engine = create_engine(settings.database_url, echo=settings.debug)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency para obtener la sesión de base de datos
def get_db():
    """Proveer una sesión de base de datos a los endpoints"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()