# 🚀 Inicio Rápido - Sistema de Reservas

## Para desarrolladores nuevos

### 1. Clonar y ejecutar setup
```bash
git clone <repo-url>
cd TP_Prog_Vanguardia

# Ejecutar setup interactivo
./setup.sh

# Opciones:
# 1) Usar configuración por defecto (más rápido)
# 2) Configurar credenciales personalizadas
```

### 2. Acceder al sistema
- **API:** http://localhost:8000
- **Documentación:** http://localhost:8000/docs
- **Base de datos (PgAdmin):** http://localhost:8080

## 🔐 Credenciales

**Al final del `setup.sh` se muestran las credenciales configuradas:**
- Usuario y password de PostgreSQL
- Email y password de PgAdmin

**También puedes consultarlas en:**
- **`docker/.env`** - Credenciales de contenedores
- **`.env`** - Configuración de la aplicación

## 🧪 Probar la API

1. Ve a http://localhost:8000/docs
2. Prueba el endpoint `GET /health`
3. Crea una persona con `POST /api/v1/personas/`
4. Lista personas con `GET /api/v1/personas/`

## 📦 Colecciones Postman

Importa el archivo `postman/Sistema_Completo_API_Collection.postman_collection.json` en Postman para testing completo.

---
**¡Listo!** El sistema debería estar funcionando con estos pasos básicos.