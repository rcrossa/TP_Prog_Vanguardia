# 🔧 Configuración del Entorno

Esta guía explica todas las variables de entorno utilizadas en el proyecto y cómo configurarlas correctamente.

## 📋 Tabla de Contenidos

- [Variables Obligatorias](#variables-obligatorias)
- [Variables Opcionales](#variables-opcionales)
- [Variables para Documentación](#variables-para-documentación)
- [Configuración por Entorno](#configuración-por-entorno)
- [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 🔴 Variables Obligatorias

Estas variables **deben** estar configuradas para que la aplicación funcione correctamente.

### Base de Datos PostgreSQL

```bash
POSTGRES_USER=reservas_user          # Usuario de PostgreSQL
POSTGRES_PASSWORD=reservas_password  # Contraseña de PostgreSQL
POSTGRES_HOST=localhost              # Host donde está PostgreSQL
POSTGRES_PORT=5432                   # Puerto de PostgreSQL
POSTGRES_DB=reservas                 # Nombre de la base de datos
```

**Nota:** Los valores por defecto funcionan con Docker Compose incluido en el proyecto.

### Seguridad y Autenticación

```bash
SECRET_KEY=dev-secret-key-change-in-production-please      # Clave para encriptación general
JWT_SECRET_KEY=dev-jwt-secret-key-change-in-production-please  # Clave para firmar tokens JWT
JWT_ALGORITHM=HS256                  # Algoritmo de firma JWT
JWT_EXPIRATION_TIME=30               # Expiración del token en MINUTOS
```

**⚠️ IMPORTANTE EN PRODUCCIÓN:**
- Cambia `SECRET_KEY` y `JWT_SECRET_KEY` por valores seguros aleatorios
- Genera claves seguras en: https://www.allkeysgenerator.com/
- **Nunca** uses las claves de ejemplo en producción
- **Nunca** compartas estas claves en repositorios públicos

---

## 🟡 Variables Opcionales

Estas variables son opcionales y tienen valores por defecto.

### Modo de Desarrollo

```bash
DEBUG=True  # Habilita modo debug (True para desarrollo, False para producción)
```

**Efectos del modo DEBUG:**
- `True`: Muestra errores detallados, recarga automática, logs verbosos
- `False`: Errores genéricos, sin recarga automática, logs mínimos (RECOMENDADO en producción)

### PgAdmin (Administrador de Base de Datos)

```bash
PGADMIN_DEFAULT_EMAIL=admin@tuorganizacion.com
PGADMIN_DEFAULT_PASSWORD=tu_password_pgadmin_seguro
```

**Uso:** Solo si planeas usar PgAdmin desde Docker Compose.

---

## 📚 Variables para Documentación (EXAMPLE_*)

Estas variables **solo afectan los ejemplos** mostrados en Swagger/OpenAPI (`http://localhost:8000/docs`).

```bash
EXAMPLE_EMAIL=juan@ejemplo.com          # Email de ejemplo para registro
EXAMPLE_USER_EMAIL=usuario@ejemplo.com  # Email de ejemplo para login
EXAMPLE_NOMBRE=Juan Pérez                # Nombre de ejemplo
EXAMPLE_PASSWORD=micontraseña123         # Contraseña de ejemplo
```

### ✅ Lo que SÍ hacen:

- Personalizan los ejemplos en la documentación Swagger
- Hacen que la API sea más amigable para testing manual
- Permiten adaptar ejemplos a tu organización

### ❌ Lo que NO hacen:

- **NO crean usuarios** en la base de datos
- **NO afectan** la lógica de autenticación
- **NO son credenciales válidas** para login
- **NO comprometen** la seguridad si se dejan por defecto

### Dónde se usan:

Archivo: `app/schemas/auth.py`

```python
# Leer datos de ejemplo desde variables de entorno
EXAMPLE_EMAIL = os.getenv("EXAMPLE_EMAIL", "juan@ejemplo.com")
EXAMPLE_USER_EMAIL = os.getenv("EXAMPLE_USER_EMAIL", "usuario@ejemplo.com")
EXAMPLE_NOMBRE = os.getenv("EXAMPLE_NOMBRE", "Juan Pérez")
EXAMPLE_PASSWORD = os.getenv("EXAMPLE_PASSWORD", "micontraseña123")

# Se usan solo en los ejemplos de Pydantic:
class UserLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"email": EXAMPLE_USER_EMAIL, "password": EXAMPLE_PASSWORD}
        }
    )
```

---

## 🌍 Configuración por Entorno

### Desarrollo Local

```bash
# .env
DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production-please
JWT_SECRET_KEY=dev-jwt-secret-key-change-in-production-please
POSTGRES_HOST=localhost
```

**Ejecutar:**
```bash
cp .env.example .env
# Usar valores por defecto (ya están configurados)
```

### Producción

```bash
# .env (NUNCA subir al repositorio)
DEBUG=False
SECRET_KEY=gAAAAABg7X9Z... (generada aleatoriamente)
JWT_SECRET_KEY=eyJ0eXAiOiJKV1... (generada aleatoriamente)
POSTGRES_HOST=db.produccion.com
POSTGRES_PASSWORD=contraseña_muy_segura_produccion
JWT_EXPIRATION_TIME=15  # Tokens más cortos en producción
```

**Checklist de producción:**
- [ ] `DEBUG=False`
- [ ] Claves `SECRET_KEY` y `JWT_SECRET_KEY` generadas aleatoriamente
- [ ] Contraseñas de base de datos seguras (mínimo 16 caracteres)
- [ ] Archivo `.env` **nunca** en el repositorio
- [ ] Variables de entorno en el sistema/contenedor (no en archivos)
- [ ] HTTPS habilitado en el servidor
- [ ] Backup de la base de datos configurado

### Testing/CI

```bash
# .env.test
DEBUG=True
POSTGRES_HOST=localhost
POSTGRES_DB=reservas_test
SECRET_KEY=test-key-only-for-ci
JWT_SECRET_KEY=test-jwt-key-only-for-ci
```

---

## 🔐 Buenas Prácticas de Seguridad

### ✅ Hacer:

1. **Usar variables de entorno del sistema** en producción (no archivos)
2. **Rotar claves** periódicamente (cada 3-6 meses)
3. **Generar claves aleatorias** de mínimo 32 caracteres
4. **Usar contraseñas fuertes** para PostgreSQL en producción
5. **Mantener** `.env` en `.gitignore`
6. **Documentar** las variables requeridas en `README.md`

### ❌ No hacer:

1. **Nunca** hardcodear claves en el código
2. **Nunca** subir archivos `.env` al repositorio
3. **Nunca** compartir claves por email/chat
4. **Nunca** usar claves de ejemplo en producción
5. **Nunca** reutilizar claves entre proyectos
6. **Nunca** dejar `DEBUG=True` en producción

---

## ❓ Preguntas Frecuentes

### ¿Debo configurar las variables EXAMPLE_* ?

**No es necesario.** Son opcionales y solo afectan la documentación Swagger. Si no las configuras, se usarán valores por defecto que funcionan perfectamente.

### ¿Cómo genero claves seguras?

**Opción 1 - Online:**
```
https://www.allkeysgenerator.com/
```

**Opción 2 - Python:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Opción 3 - OpenSSL:**
```bash
openssl rand -base64 32
```

### ¿Qué pasa si cambio JWT_SECRET_KEY?

**Todos los tokens existentes se invalidarán.** Los usuarios deberán volver a iniciar sesión. Esto es útil para:
- Revocar todos los tokens en caso de compromiso
- Cerrar sesiones de todos los usuarios
- Rotación de claves de seguridad

### ¿Por qué los ejemplos muestran contraseñas en texto plano?

Los valores `EXAMPLE_PASSWORD` son **solo para documentación visual** en Swagger. Las contraseñas reales en la base de datos **siempre** se hashean con bcrypt antes de guardarse.

### ¿Puedo cambiar el tiempo de expiración del token?

Sí, ajusta `JWT_EXPIRATION_TIME`:
- **Desarrollo:** 30-60 minutos (más cómodo)
- **Producción:** 15-30 minutos (más seguro)
- **APIs públicas:** 5-10 minutos (muy seguro)

**Nota:** El valor está en **minutos**, pero se convierte a segundos internamente.

### ¿Cómo verifico que las variables están cargadas?

**Opción 1 - En Python:**
```python
from app.core.config import settings
print(settings.POSTGRES_USER)
print(settings.JWT_EXPIRATION_TIME)
```

**Opción 2 - Endpoint de salud:**
```bash
curl http://localhost:8000/api/v1/health
```

---

## 📁 Archivos Relacionados

| Archivo | Propósito |
|---------|-----------|
| `.env.example` | Plantilla con valores de ejemplo |
| `.env` | Configuración real (no subir al git) |
| `app/core/config.py` | Carga y valida variables de entorno |
| `app/schemas/auth.py` | Define variables EXAMPLE_* |
| `docker/.env` | Variables para Docker Compose |

---

## 🔗 Referencias

- [FastAPI Settings Management](https://fastapi.tiangolo.com/advanced/settings/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [OWASP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

---

**Última actualización:** Noviembre 2025  
**Autor:** Equipo de Desarrollo
