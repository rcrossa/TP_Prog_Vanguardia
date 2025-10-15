# 🚀 Inicio Rápido - Sistema de Reservas

## Para desarrolladores nuevos

### 1. Clonar y ejecutar setup
```bash
git clone <repo-url>
cd TP_Prog_Vanguardia

# El setup crea automáticamente los archivos .env necesarios
./setup.sh
```

### 2. Acceder al sistema
- **API:** http://localhost:8000
- **Documentación:** http://localhost:8000/docs
- **Base de datos (PgAdmin):** http://localhost:8080

## � Credenciales

Las credenciales se generan automáticamente en:
- **`.env`** - Configuración de la aplicación
- **`docker/.env`** - Configuración de contenedores

> 💡 **Para ver las credenciales:** Revisa el archivo `.env` después de ejecutar `setup.sh`

## 🧪 Probar la API

1. Ve a http://localhost:8000/docs
2. Prueba el endpoint `GET /health`
3. Crea una persona con `POST /api/v1/personas/`
4. Lista personas con `GET /api/v1/personas/`

## 📦 Colecciones Postman

Importa el archivo `postman/Sistema_Completo_API_Collection.postman_collection.json` en Postman para testing completo.

---
**¡Listo!** El sistema debería estar funcionando con estos pasos básicos.