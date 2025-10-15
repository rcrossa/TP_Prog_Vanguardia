# 🔒 Configuración de Seguridad

## 📋 Configuración Segura Implementada

### Variables de Entorno
El sistema utiliza variables de entorno para todas las configuraciones sensibles. No hay credenciales hardcodeadas en el código.

**Configuración en `app/core/config.py`:**
```python
class Settings(BaseSettings):
    # Base de datos
    postgres_user: str = Field(..., env="POSTGRES_USER")
    postgres_password: str = Field(..., env="POSTGRES_PASSWORD")
    postgres_db: str = Field(..., env="POSTGRES_DB")
    postgres_host: str = Field("localhost", env="POSTGRES_HOST")
    postgres_port: int = Field(5432, env="POSTGRES_PORT")
    
    # Seguridad
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
```

### Variables de Entorno Requeridas
```bash
# Base de datos
POSTGRES_USER=usuario_bd
POSTGRES_PASSWORD=contraseña_segura  
POSTGRES_DB=nombre_base_datos
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Seguridad
SECRET_KEY=clave_secreta_muy_larga_y_segura
```

### Archivos de Configuración
- **`.env`**: Archivo local con variables reales (en `.gitignore`)
- **`.env.example`**: Plantilla sin datos sensibles
- **`docker/.env.example`**: Plantilla para Docker Compose

## �️ Mejores Prácticas Implementadas

### Desarrollo Local
1. Copiar `.env.example` a `.env`
2. Completar con valores reales
3. El archivo `.env` está en `.gitignore` y no se commitea

### Producción
1. Configurar variables de entorno del sistema
2. Usar servicios de gestión de secretos cuando sea posible
3. Rotar credenciales regularmente

### Docker Compose
El archivo `docker-compose.yml` utiliza substitución de variables:
```yaml
environment:
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-reservas_password}
  POSTGRES_USER: ${POSTGRES_USER:-reservas_user}
```

## 🚀 Configuración Rápida

### Para Desarrollo
```bash
# 1. Copiar archivo de ejemplo
cp .env.example .env

# 2. Editar con tus valores
# 3. Ejecutar la aplicación
python main.py
```

### Para Docker
```bash
# 1. Configurar variables para Docker
cp docker/.env.example docker/.env

# 2. Editar docker/.env con tus valores
# 3. Levantar contenedores
cd docker && docker-compose up -d
```