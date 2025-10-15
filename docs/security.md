# 🔒 Configuración de Seguridad

## ⚠️ Problema Identificado

En el primer commit se incluyeron credenciales de base de datos directamente en el código fuente, lo cual representa una vulnerabilidad de seguridad.

## ✅ Solución Implementada

### 1. Configuración Centralizada
- Creado `app/core/config.py` con clase `Settings`
- Todas las configuraciones sensibles provienen de variables de entorno
- Validación obligatoria de variables críticas

### 2. Variables de Entorno Obligatorias
```bash
POSTGRES_USER=tu_usuario
POSTGRES_PASSWORD=tu_contraseña  
POSTGRES_DB=tu_base_de_datos
SECRET_KEY=tu_clave_secreta
JWT_SECRET_KEY=tu_jwt_secret
```

### 3. Archivos Protegidos
- `.env` está en `.gitignore` (no se sube al repositorio)
- `.env.example` es la plantilla sin datos sensibles
- `config.py` valida que las variables existan

## 🚨 Recomendaciones de Seguridad

### Desarrollo Local
1. Copiar `.env.example` a `.env`
2. Completar con valores reales
3. Nunca commitear el archivo `.env`

### Producción
1. Usar variables de entorno del sistema
2. Usar servicios de gestión de secretos (AWS Secrets Manager, etc.)
3. Rotar credenciales regularmente

### Gestión de Secretos
- **✅ Correcto:** Variables de entorno, servicios de secretos
- **❌ Incorrecto:** Hardcodeado en código, archivos de configuración en repo

## 🔄 Migración Aplicada

```python
# ❌ ANTES (inseguro)
POSTGRES_PASSWORD = "reservas_password"

# ✅ DESPUÉS (seguro)  
postgres_password = os.getenv("POSTGRES_PASSWORD")
if not postgres_password:
    raise ValueError("POSTGRES_PASSWORD es requerida")
```