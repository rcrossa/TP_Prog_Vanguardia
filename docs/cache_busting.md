# 🔄 Sistema de Cache Busting Automático

## 📋 ¿Qué es Cache Busting?

El **cache busting** es una técnica para forzar que los navegadores descarguen las versiones más recientes de archivos estáticos (CSS, JavaScript) en lugar de usar versiones antiguas en caché.

## ⚙️ Cómo Funciona en Este Proyecto

### 1. **Durante el Setup**
Cuando ejecutas `./setup_inicia_todo.sh`, el script:

```bash
# Genera un timestamp único
CACHE_VERSION=$(date +%s)  # Ej: 1762948503

# Lo agrega a .env y docker/.env
STATIC_VERSION=1762948503
```

### 2. **En la Aplicación Python**
El archivo `app/web/routes.py` lee esta variable:

```python
STATIC_VERSION = os.getenv('STATIC_VERSION')
if not STATIC_VERSION:
    # Si no existe, usa timestamp del inicio de la app
    STATIC_VERSION = str(int(datetime.now().timestamp()))
```

### 3. **En los Templates HTML**
Los archivos usan la variable Jinja `{{ static_version }}`:

```html
<!-- Antes -->
<script src="/static/js/reservas/reservas.js"></script>

<!-- Ahora -->
<script src="/static/js/reservas/reservas.js?v={{ static_version }}"></script>

<!-- Renderizado final -->
<script src="/static/js/reservas/reservas.js?v=1762948503"></script>
```

## 🎯 ¿Cuándo se Invalida la Caché?

La caché del navegador se invalida automáticamente en estas situaciones:

### ✅ **Escenario 1: Nuevo Setup**
```bash
./setup_inicia_todo.sh
# Genera nuevo STATIC_VERSION → Navegadores descargan archivos nuevos
```

### ✅ **Escenario 2: Reinicio del Contenedor**
Si `STATIC_VERSION` no está configurada en el `.env`, se genera una nueva al iniciar:

```bash
docker-compose restart python-service
# Genera timestamp del momento de inicio
```

### ✅ **Escenario 3: Rebuild de la Imagen**
```bash
docker-compose up -d --build python-service
# Nueva imagen = nuevo contexto = nueva versión
```

## 📁 Archivos Modificados

### **Scripts de Setup**
- `setup_inicia_todo.sh` - Genera `STATIC_VERSION` automáticamente
- `.env.example` - Documenta la variable

### **Código Python**
- `app/web/routes.py` - Lee y configura `STATIC_VERSION` en templates
- `docker/docker-compose.full.yml` - Pasa variable al contenedor

### **Templates HTML**
Todos los templates ahora usan `{{ static_version }}`:
- `templates/base.html` - CSS y JS globales
- `templates/login.html` - Página de login
- `templates/reservas.html` - JavaScript de reservas
- `templates/inventario.html` - JavaScript de inventario

## 🧪 Cómo Probar

### **1. Verificar la versión actual**
```bash
# Ver versión en .env
grep STATIC_VERSION .env

# Ver versión en el HTML
curl -s http://localhost:8000/login | grep "auth.js?v="
```

### **2. Forzar nueva versión manualmente**
```bash
# Opción A: Editar .env
echo "STATIC_VERSION=$(date +%s)" >> .env

# Opción B: Volver a ejecutar setup
./setup_inicia_todo.sh

# Reiniciar contenedor
docker-compose -f docker/docker-compose.full.yml restart python-service
```

### **3. Verificar que cambió**
```bash
curl -s http://localhost:8000/login | grep "auth.js?v="
# Deberías ver un número diferente
```

## 🚀 Ventajas de Este Sistema

### ✅ **Automático**
- No necesitas cambiar manualmente las versiones en los archivos
- Cada setup genera una versión única

### ✅ **Sin Cambios en Git**
- Los números de versión no se commitean
- Solo se modifican archivos `.env` (ignorados por git)

### ✅ **Desarrollo Limpio**
- No afecta el workflow de desarrollo
- Funciona tanto en Docker como en entorno local

### ✅ **Producción Ready**
- En producción: `STATIC_VERSION` fijo en el `.env`
- En desarrollo: Se regenera automáticamente

## 💡 Tips

### **Durante Desarrollo**
Si estás modificando JavaScript frecuentemente:

```bash
# Opción 1: Hard refresh en el navegador
# Mac: Cmd + Shift + R
# Windows: Ctrl + Shift + R

# Opción 2: Regenerar versión
echo "STATIC_VERSION=$(date +%s)" > .env
docker-compose restart python-service
```

### **Para Producción**
Fija una versión específica en el `.env`:

```bash
# .env de producción
STATIC_VERSION=v1.0.0
# O usa la fecha de release
STATIC_VERSION=20250112
```

## 🔧 Troubleshooting

### **Problema: Los cambios en JS no se reflejan**
```bash
# 1. Verifica que STATIC_VERSION esté configurada
docker exec reservas_python_full env | grep STATIC

# 2. Verifica que el HTML use la versión
curl -s http://localhost:8000/login | grep "\.js?v="

# 3. Si no aparece, rebuild
docker-compose -f docker/docker-compose.full.yml up -d --build python-service
```

### **Problema: Versión siempre es "1"**
Esto significa que `STATIC_VERSION` no está en `docker/.env`:

```bash
# Agregar manualmente
echo "STATIC_VERSION=$(date +%s)" >> docker/.env
docker-compose restart python-service
```

## 📚 Referencias

- [MDN: HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)
- [Google: Cache Busting](https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/http-caching#invalidating_and_updating_cached_responses)
