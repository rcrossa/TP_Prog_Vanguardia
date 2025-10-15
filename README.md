# 🏢 Sistema de Reservas de Salas

## 📚 Información Académica

- **Asignatura:** Programación de Vanguardia  
- **Carrera:** Licenciatura en Tecnologías Informáticas
- **Ciclo Lectivo:** 2025

## 📖 Descripción

Sistema moderno para la gestión de reservas de salas y recursos organizacionales, desarrollado con tecnologías actuales y mejores prácticas de desarrollo.

### �️ Tecnologías Utilizadas

- **Backend:** FastAPI (Python)
- **ORM:** SQLAlchemy 2.0 con Mapped types
- **Base de Datos:** PostgreSQL
- **Validación:** Pydantic v2
- **Containerización:** Docker & Docker Compose
- **Testing:** Postman Collections

## ⚡ Funcionalidades

### 👥 Gestión de Personas
- CRUD completo de usuarios
- Validación de emails únicos
- Información de contacto y departamento

### 🏛️ Administración de Salas  
- Gestión de espacios con capacidades
- Información de ubicación y equipamiento
- Filtros por capacidad mínima

### � Inventario de Artículos
- Control de artículos reservables
- Estados de disponibilidad
- Categorización por tipo

### 📅 Sistema de Reservas
- Reservas de salas y artículos
- Validación de conflictos de horarios
- Gestión de estados de reserva

## 🗃️ Modelo de Datos

El sistema maneja cuatro entidades principales:

- **👥 Personas** - Usuarios del sistema con nombre y email único
- **🏛️ Salas** - Espacios físicos con capacidad definida  
- **📦 Artículos** - Equipamiento reservable con estado de disponibilidad
- **📅 Reservas** - Vinculación de personas con salas/artículos en fechas específicas

### Relaciones
- Una **reserva** pertenece a una **persona** (obligatorio)
- Una **reserva** puede ser de una **sala** O un **artículo** (exclusivo)
- Las **reservas** incluyen fecha/hora de inicio y fin

## � Instalación y Uso

### Requisitos Previos
- Python 3.11+
- Docker y Docker Compose
- Git

### Instalación Rápida
```bash
# 1. Clonar repositorio
git clone <repo-url>
cd TP_Prog_Vanguardia

# 2. Ejecutar setup interactivo
./setup.sh
# El script te preguntará si usar valores por defecto o configurar credenciales personalizadas

# 3. Acceder a la aplicación
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
# PgAdmin: http://localhost:8080
```

### 🔐 Opciones de Configuración

El script `setup.sh` te ofrece dos opciones:

**Opción 1: Configuración por defecto (recomendada)**
- Usa valores seguros predefinidos para desarrollo
- No requiere edición manual
- Perfecto para comenzar rápidamente

**Opción 2: Credenciales personalizadas**
- Te permite editar `.env` y `docker/.env` 
- Para usuarios que quieren credenciales específicas
- El script espera a que termines de editarlos

> 💡 **Al final del setup:** Se muestran las credenciales que están siendo utilizadas

### Configuración Manual
```bash
# Base de datos con Docker
cd docker && docker-compose up -d

# Entorno Python
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Ejecutar aplicación
python main.py
```

## 🧪 Testing

### Postman Collections
El directorio `postman/` contiene colecciones completas para testing:
- Testing de todos los endpoints
- Casos de uso avanzados  
- Validación de errores

### Verificación de Calidad
```bash
# Script de verificación automática
./scripts/check_code_quality.sh
```

## � Documentación

- **`docs/architecture.md`** - Arquitectura del sistema
- **`docs/security.md`** - Configuración de seguridad
- **`docs/formato_codigo.md`** - Estándares de código
- **API Docs** - http://localhost:8000/docs (FastAPI auto-docs)

## 🔒 Seguridad

- ✅ Variables de entorno para credenciales
- ✅ Sin hardcoding de passwords
- ✅ Validación de entrada con Pydantic
- ✅ Configuración centralizada
- **Fase 3:** Implementación del módulo de predicción
- **Fase 4:** Pruebas y optimización
- **Fase 5:** Despliegue y documentación

## 📄 Licencia

[Información de licencia]

## 🤝 Contribución

[Guías para contribuir al proyecto]

---

*Proyecto desarrollado como parte del trabajo práctico de Programación de Vanguardia - Universidad CAECE*