"""
Configuración centralizada de la aplicación.

Este módulo maneja todas las variables de entorno y configuraciones
del sistema de reservas, incluyendo base de datos, JWT y seguridad.
"""

import os

from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()


class Settings:
    """
    Configuración centralizada de la aplicación.

    Maneja todas las variables de entorno necesarias para la aplicación,
    incluyendo configuración de base de datos, JWT y seguridad.
    Las variables críticas son requeridas sin valores por defecto.
    """

    # Base de datos - REQUERIDAS (sin valores por defecto por seguridad)
    postgres_user: str = os.getenv("POSTGRES_USER") or ""
    postgres_password: str = os.getenv("POSTGRES_PASSWORD") or ""
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: str = os.getenv("POSTGRES_PORT", "5432")
    postgres_db: str = os.getenv("POSTGRES_DB") or ""

    # Aplicación
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    secret_key: str = os.getenv("SECRET_KEY") or ""

    # JWT
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY") or ""
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expiration_time: int = int(os.getenv("JWT_EXPIRATION_TIME", "30"))

    @property
    def database_url(self) -> str:
        """Construir URL de base de datos"""
        missing_vars = []
        if not self.postgres_user:
            missing_vars.append("POSTGRES_USER")
        if not self.postgres_password:
            missing_vars.append("POSTGRES_PASSWORD")
        if not self.postgres_db:
            missing_vars.append("POSTGRES_DB")

        if missing_vars:
            raise ValueError(
                f"Variables de entorno requeridas faltantes: {', '.join(missing_vars)}. "
                f"Por favor configúrelas en el archivo .env"
            )

        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    def validate_required_settings(self) -> None:
        """Validar que todas las configuraciones críticas estén presentes"""
        missing_vars = []

        if not self.secret_key:
            missing_vars.append("SECRET_KEY")
        if not self.jwt_secret_key:
            missing_vars.append("JWT_SECRET_KEY")

        if missing_vars:
            raise ValueError(
                f"Variables de entorno de seguridad faltantes: {', '.join(missing_vars)}. "
                f"Por favor configúrelas en el archivo .env"
            )


# Instancia global de configuración
settings = Settings()
