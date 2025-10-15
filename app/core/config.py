import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Settings:
    # Base de datos
    postgres_user: str = os.getenv("POSTGRES_USER")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD")
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: str = os.getenv("POSTGRES_PORT", "5432")
    postgres_db: str = os.getenv("POSTGRES_DB")
    
    # Aplicación
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    secret_key: str = os.getenv("SECRET_KEY")
    
    # JWT
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expiration_time: int = int(os.getenv("JWT_EXPIRATION_TIME", "30"))
    
    @property
    def database_url(self) -> str:
        """Construir URL de base de datos"""
        if not all([self.postgres_user, self.postgres_password, self.postgres_db]):
            raise ValueError(
                "Variables de entorno requeridas: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB"
            )
        
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

# Instancia global de configuración
settings = Settings()