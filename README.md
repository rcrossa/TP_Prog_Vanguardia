# 🏢 Sistema de Reservas - Arquitectura Microservicios

> 🚀 **¿Primera vez?** Ve a la sección **[🚀 Inicio Rápido](#-inicio-rápido)** más abajo para poner el proyecto en marcha.

## 📚 Información Académica

- **Asignatura:** Programación de Vanguardia  
- **Carrera:** Licenciatura en Tecnologías Informáticas
- **Ciclo Lectivo:** 2025

## 📖 Descripción

Sistema moderno de gestión de reservas implementado con **arquitectura de microservicios**, combinando **Python (FastAPI)** para operaciones CRUD y autenticación, con **Java (Spring Boot)** para gestión de recursos físicos e inventario.

### 📑 Navegación Rápida

| Para... | Ve a... |
|---------|---------|
| 🚀 **Ejecutar el proyecto** | [🚀 Inicio Rápido](#-inicio-rápido) (en este README) |
| 📖 **Entender la arquitectura** | [docs/architecture.md](./docs/architecture.md) |
|  **Configurar Docker** | [docker/README.md](./docker/README.md) |
| ☕ **Java Service (API)** | [java-service/README.md](./java-service/README.md) |

### 📊 Estado Actual del Proyecto

**Última actualización:** Octubre 2025  
**Progreso General:** 🟢 **~75% Completado**

#### ✅ Componentes Funcionales

// ...existing code...

---

// ...existing code...
DATABASE_URL=postgresql://[user]:[password]@localhost:5432/reservas
```

> 💡 **Tip:** Revisa `docker/.env.example` para las credenciales de desarrollo locales

#### ❌ "Module not found" (Python)

**Problema:** Dependencias no instaladas.

**Solución:**
```bash
pip install -r requirements.txt

# Si falla, actualizar pip:
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### 🛑 Detener el Sistema

**Detener servicios Python/Java:**
- Presiona `Ctrl + C` en cada terminal

**Detener Docker:**

**🪟 Windows:**
```powershell
cd docker
docker-compose -f docker-compose.db-only.yml down
```

**🍎 macOS / 🐧 Linux:**
```bash
cd docker
./stop-all.sh
```

---

## 🏗️ Arquitectura del Sistema

```mermaid
graph TB
    subgraph Frontend["🌐 FRONTEND WEB"]
        UI[React/Vue/Angular<br/>Templates HTML + JavaScript]
    end

    subgraph Python["🐍 PYTHON SERVICE<br/>FastAPI - Port 8000"]
        P1[👤 ABM Usuarios]
        P2[📅 Sistema Reservas]
        P3[🔐 Autenticación JWT]
        P4[🤖 Predicción ML]
        P5[📈 Analytics]
        P6[📊 Reportes Avanzados]
    end

    subgraph Java["☕ JAVA SERVICE<br/>Spring Boot - Port 8080"]
        J1[🏢 ABM Salas]
        J2[� ABM Artículos]
    end

    subgraph Database["🗄️ PostgreSQL<br/>Port 5432"]
        DB[(Base de Datos)]
        T1[Personas]
        T2[Salas]
        T3[Articulos]
        T4[Reservas]
        T5[Analytics]
    end

    UI --> Python
    UI --> Java
    Python --> DB
    Java --> DB
    Python -.->|Llamadas API| Java
    Java -.->|Validación Auth| Python

    style Frontend fill:#e1f5ff
    style Python fill:#d4edda
    style Java fill:#fff3cd
    style Database fill:#f8d7da
```

## 📋 Distribución de Responsabilidades

### 🐍 Python Service (Port 8000)
| Módulo | Funcionalidad | Estado |
|--------|---------------|--------|
| 👤 **ABM Usuarios** | Gestión completa de personas + Auth JWT | ✅ Implementado |
| 📅 **Sistema Reservas** | Creación y gestión de reservas | ✅ Implementado |
| 🔐 **Autenticación** | Login, JWT, roles (admin/usuario) | ✅ Implementado |
| 🎨 **Frontend Web** | Templates HTML + JavaScript | ✅ Implementado |
| 🤖 **Predicción ML** | Análisis y predicción de demanda con scikit-learn | ⏳ Pendiente |
| � **Analytics** | Métricas, estadísticas y patrones de uso | ⏳ Pendiente |
| 📊 **Reportes Avanzados** | Generación de informes complejos (PDF/Excel) | ⏳ Pendiente |

### ☕ Java Service (Port 8080)
| Módulo | Funcionalidad | Estado |
|--------|---------------|--------|
| 🏢 **ABM Salas** | CRUD completo de espacios reservables | ✅ Implementado |
| 📦 **ABM Artículos** | CRUD completo de recursos/inventario | ✅ Implementado |
| 📚 **API REST** | Endpoints REST con validación | ✅ Implementado |
| 📖 **Swagger/OpenAPI** | Documentación interactiva de API | ✅ Implementado |
| 🐳 **Dockerización** | Dockerfile y compilación JAR | ✅ Implementado |
| 🧪 **Testing** | Tests unitarios e integración | ⏳ Pendiente |

### ️ Tecnologías Utilizadas

#### Python Stack
- **Backend:** FastAPI
- **ORM:** SQLAlchemy 2.0 con Mapped types
- **Validación:** Pydantic v2
- **Auth:** JWT (JSON Web Tokens)
- **Templates:** Jinja2
- **Data Science:** pandas, numpy, scikit-learn
- **Visualización:** matplotlib, plotly
- **Reportes:** reportlab (PDF), openpyxl (Excel)

#### Java Stack (✅ Implementado)
- **Backend:** Spring Boot 3.3.0 con Java 17
- **ORM:** Spring Data JPA + Hibernate
- **Base de Datos:** PostgreSQL Driver
- **Build:** Maven 3.6+
- **Documentación:** SpringDoc OpenAPI (Swagger)
- **Lombok:** Reducción de boilerplate
- **Validación:** Spring Boot Validation
- **Testing:** JUnit 5 (estructura lista, tests pendientes)

#### Infraestructura
- **Base de Datos:** PostgreSQL 15
- **Containerización:** Docker & Docker Compose
- **Testing:** Postman Collections

## 📚 Documentación del Proyecto

Este proyecto cuenta con documentación completa organizada por módulos:

### 📖 Guías Principales

| Documento | Descripción | Enlace |
|-----------|-------------|--------|
| 🚀 **Inicio Rápido** | Instalación y configuración multi-plataforma | [🚀 Inicio Rápido](#-inicio-rápido) (en este README) |
| 🐳 **Docker** | Guía completa de uso con contenedores | [`docker/README.md`](./docker/README.md) |
| ☕ **Java Service** | API y documentación del microservicio Java | [`java-service/README.md`](./java-service/README.md) |
| 🏗️ **Arquitectura** | Diseño y patrones del sistema | [`docs/architecture.md`](./docs/architecture.md) |
| 🔐 **Seguridad** | Mejores prácticas y configuración | [`docs/security.md`](./docs/security.md) |
| 📝 **Cambios Recientes** | Detalle de últimas implementaciones | [`docs/CAMBIOS_RECIENTES.md`](./docs/CAMBIOS_RECIENTES.md) |
| ✅ **Checklist General** | Verificación completa del proyecto | [`docs/CHECKLIST_GENERAL.md`](./docs/CHECKLIST_GENERAL.md) |
| 💾 **Base de Datos** | Scripts SQL y configuración | [`docker/init-scripts/README.md`](./docker/init-scripts/README.md) |
| 📮 **Postman** | Colecciones para testing de API | [`postman/README.md`](./postman/README.md) |
| 🧪 **Testing** | Guías de pruebas y calidad | [`tests/README.md`](./tests/README.md) |
| 📜 **Scripts** | Herramientas y utilidades del proyecto | [`scripts/README.md`](./scripts/README.md) |

### 🎯 Guías por Perfil

#### Para Desarrolladores
1. Clonar repo y seguir la guía [🚀 Inicio Rápido](#-inicio-rápido)
2. Configurar entorno con [`docker/README.md`](./docker/README.md)
3. Entender arquitectura en [`docs/architecture.md`](./docs/architecture.md)
4. Seguir formato de código en [`docs/formato_codigo.md`](./docs/formato_codigo.md)

#### Para Evaluadores/Profesores
1. Ver **Estado Actual del Proyecto** (sección anterior de este README)
2. Ver cambios recientes en [`docs/CAMBIOS_RECIENTES.md`](./docs/CAMBIOS_RECIENTES.md)
3. Ejecutar con [`docker/README.md`](./docker/README.md) - Sección "Guía para Evaluadores"
4. Probar APIs con colecciones en [`postman/README.md`](./postman/README.md)
5. Revisar arquitectura en [`docs/architecture.md`](./docs/architecture.md)

#### Para Usuarios Finales
1. Acceso al sistema: `http://localhost:8000`
2. Credenciales de prueba (ver [`docker/init-scripts/README.md`](./docker/init-scripts/README.md))
3. Manual de uso (próximamente)

---

## ⚡ Funcionalidades

### ✅ Implementadas en Python Service

#### 👥 Gestión de Personas (Usuarios)

#### 🏛️ Administración de Salas  

#### 📅 Sistema de Reservas
    - ✅ Visualización de detalles de reserva mediante modal Bootstrap (mejora UX)
    - ✅ Lógica de stock de artículos considera solo reservas futuras (no bloquea por reservas pasadas)

### ⏳ Pendientes en Python Service

#### 🤖 Predicción ML
- ⏳ Análisis de patrones con scikit-learn
- ⏳ Predicción de demanda futura
- ⏳ Optimización de recursos
- ⏳ Identificación de horarios pico
- ⏳ Modelos de clasificación y regresión

#### 📈 Analytics
- ⏳ Dashboard de métricas en tiempo real
- ⏳ Tendencias de uso con pandas
- ⏳ Heatmap de reservas
- ⏳ KPIs del sistema
- ⏳ Análisis de comportamiento de usuarios

#### 📊 Reportes Avanzados
- ⏳ Reportes por período
- ⏳ Recursos más utilizados
- ⏳ Tasa de ocupación
- ⏳ Exportación a PDF (reportlab)
- ⏳ Exportación a Excel (openpyxl)
- ⏳ Gráficos y visualizaciones

### ✅ Implementadas en Java Service

#### 🏢 ABM de Salas
- ✅ CRUD completo de salas (GET, POST, PUT, DELETE)
- ✅ Búsqueda por nombre y capacidad
- ✅ Filtrado por disponibilidad
- ✅ Validación de datos con DTOs
- ✅ Repositorio JPA con Spring Data
- ✅ Control de disponibilidad

#### 📦 ABM de Artículos
- ✅ CRUD completo de artículos (GET, POST, PUT, DELETE)
- ✅ Búsqueda por nombre
- ✅ Filtrado por categoría
- ✅ Filtrado por disponibilidad
- ✅ Control de stock/cantidad
- ✅ Validación de datos con DTOs
- ✅ Gestión de inventario

#### 🔧 Infraestructura Java
- ✅ Spring Boot 3.3.0 con Java 17
- ✅ Spring Data JPA + PostgreSQL
- ✅ Lombok para reducción de código
- ✅ Configuración CORS para integración
- ✅ Swagger/OpenAPI para documentación
- ✅ Manejo centralizado de excepciones
- ✅ JAR compilado y listo (53.6 MB)
- ✅ Dockerfile para containerización

### ⏳ Pendientes en Java Service

#### 🧪 Testing
- ⏳ Tests unitarios con JUnit 5
- ⏳ Tests de integración
- ⏳ Tests de repositorio
- ⏳ Tests de controladores

#### 🔗 Integración
- ⏳ Comunicación activa con Python service
- ⏳ Validación de tokens JWT desde Python
- ⏳ Sincronización de datos de reservas

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

El script `setup.sh` para mac te ofrece dos opciones:

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

## 🔄 Comunicación entre Servicios

> ✅ **Estado:** **INTEGRACIÓN ACTIVA Y FUNCIONAL**

### Java → Python (✅ IMPLEMENTADO)
El servicio Java **llama a Python** para:
- ✅ **Validar tokens de autenticación JWT** al crear salas/artículos
- ✅ **Verificar permisos de usuarios** autenticados
- ✅ **Obtener información de usuarios** para auditoría


### Python → Java (✅ IMPLEMENTADO)
El servicio Python **llama a Java** para:
- ✅ **Validar salas disponibles** al crear reservas
- ✅ **Consultar información de salas** en tiempo real
- ✅ **Verificar existencia de recursos** antes de reservar


### 🔗 Endpoints de Demostración

**Prueba la integración funcionando:**
```bash
# Ver endpoints de integración activos
GET http://localhost:8000/api/v1/integration/demo
GET http://localhost:8000/api/v1/integration/salas
GET http://localhost:8000/api/v1/integration/test-java-call
```

> 🧪 **Script de testing:** Ejecuta `./scripts/test_integration.sh` para verificar que la integración funciona correctamente.

---

## 📡 APIs Disponibles

### Python Service (Port 8000)

#### Autenticación
- `POST /api/v1/personas/login` - Login con JWT
- `POST /api/v1/personas/web-login` - Login web con cookies
- `GET /api/v1/personas/me` - Usuario actual

#### Personas
- `GET /api/v1/personas` - Listar usuarios
- `POST /api/v1/personas` - Crear usuario
- `GET /api/v1/personas/{id}` - Obtener usuario
- `PUT /api/v1/personas/{id}` - Actualizar
- `DELETE /api/v1/personas/{id}` - Eliminar

#### Salas
- `GET /api/v1/salas` - Listar salas
- `POST /api/v1/salas` - Crear sala
- `GET /api/v1/salas/{id}` - Obtener sala
- `PUT /api/v1/salas/{id}` - Actualizar
- `DELETE /api/v1/salas/{id}` - Eliminar

#### Reservas
- `GET /api/v1/reservas` - Listar reservas
- `POST /api/v1/reservas` - Crear reserva
- `GET /api/v1/reservas/{id}` - Obtener reserva
- `PUT /api/v1/reservas/{id}` - Actualizar
- `DELETE /api/v1/reservas/{id}` - Eliminar

### Java Service (Port 8080) - ✅ Implementado

#### Salas
- ✅ `GET /api/salas` - Listar todas las salas
- ✅ `GET /api/salas/{id}` - Obtener sala por ID
- ✅ `GET /api/salas/disponibles` - Salas disponibles
- ✅ `GET /api/salas/search?nombre=X` - Buscar por nombre
- ✅ `GET /api/salas/capacidad/{min}` - Por capacidad mínima
- ✅ `POST /api/salas` - Crear sala
- ✅ `PUT /api/salas/{id}` - Actualizar sala
- ✅ `DELETE /api/salas/{id}` - Eliminar sala

#### Artículos
- ✅ `GET /api/articulos` - Listar todos los artículos
- ✅ `GET /api/articulos/{id}` - Obtener artículo por ID
- ✅ `GET /api/articulos/disponibles` - Artículos disponibles
- ✅ `GET /api/articulos/categoria/{cat}` - Por categoría
- ✅ `GET /api/articulos/search?nombre=X` - Buscar por nombre
- ✅ `POST /api/articulos` - Crear artículo
- ✅ `PUT /api/articulos/{id}` - Actualizar artículo
- ✅ `DELETE /api/articulos/{id}` - Eliminar artículo

#### Documentación
- ✅ `GET /swagger-ui.html` - Swagger UI interactivo
- ✅ `GET /api-docs` - OpenAPI JSON

### Python Service (Port 8000) - Analytics/ML - ⏳ Propuesto

#### Reportes (Pendiente)
- ⏳ `GET /api/v1/reportes/reservas-por-periodo`
- ⏳ `GET /api/v1/reportes/recursos-mas-usados`
- ⏳ `GET /api/v1/reportes/utilizacion-salas`
- ⏳ `GET /api/v1/reportes/export/pdf`
- ⏳ `GET /api/v1/reportes/export/excel`

#### Predicción ML (Pendiente)
- ⏳ `GET /api/v1/prediction/demand/{resourceId}`
- ⏳ `GET /api/v1/prediction/peak-hours`
- ⏳ `GET /api/v1/prediction/optimal-allocation`
- ⏳ `POST /api/v1/prediction/train-model`

#### Analytics (Pendiente)
- ⏳ `GET /api/v1/analytics/usage-patterns`
- ⏳ `GET /api/v1/analytics/trends`
- ⏳ `GET /api/v1/analytics/dashboard`
- ⏳ `GET /api/v1/analytics/heatmap`

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

## 📚 Documentación

- **`docs/architecture.md`** - Arquitectura completa de microservicios
- **`docs/security.md`** - Configuración de seguridad
- **`docs/formato_codigo.md`** - Estándares de código
- **API Docs Python** - http://localhost:8000/docs (Swagger UI)
- **API Docs Java** - http://localhost:8080/swagger-ui.html (cuando esté implementado)

## 🔒 Seguridad

- ✅ Variables de entorno para credenciales
- ✅ Sin hardcoding de passwords
- ✅ JWT con cookies HTTP-only
- ✅ Control de acceso basado en roles
- ✅ Validación de entrada con Pydantic
- ✅ CORS configurado correctamente

## 🗺️ Roadmap del Proyecto

### ✅ Fase 1: Python Service - Base COMPLETADA
- [x] Configuración de FastAPI
- [x] Modelos SQLAlchemy 2.0
- [x] ABM de Usuarios (Personas)
- [x] ABM de Salas (temporalmente, se migrará a Java)
- [x] Sistema de Reservas
- [x] Autenticación JWT + Cookies
- [x] Frontend Web con templates
- [x] Control de roles (admin/usuario)

### ✅ Fase 2: Java Service - COMPLETADA
- [x] Setup de Spring Boot 3.3.0 + Java 17
- [x] Configuración de PostgreSQL con JPA
- [x] Implementar ABM de Salas (8 endpoints)
- [x] Implementar ABM de Artículos (8 endpoints)
- [x] APIs REST con validación de DTOs
- [x] Swagger/OpenAPI para documentación
- [x] Dockerfile y compilación JAR
- [x] Configuración CORS
- [ ] Tests unitarios (JUnit 5)
- [ ] Validación de tokens con Python service
- [ ] Integración activa Python ↔ Java

### ⏳ Fase 3: Analytics y ML en Python - PENDIENTE
- [ ] Módulo de Analytics con pandas
- [ ] Dashboard de métricas en tiempo real
- [ ] Análisis de patrones históricos
- [ ] Modelos de predicción (scikit-learn)
- [ ] Algoritmos de optimización de recursos
- [ ] Identificación de horarios pico

### ⏳ Fase 4: Reportes Avanzados en Python - PENDIENTE
- [ ] Sistema de reportes avanzados
- [ ] Generación de PDF (reportlab)
- [ ] Exportación a Excel (openpyxl)
- [ ] Gráficos y visualizaciones
- [ ] Reportes programados

### ✅ Fase 5: Integración y Despliegue - COMPLETADA
- [x] Comunicación Python ↔ Java (HTTP clients) ✅
- [x] Validación JWT cross-service ✅
- [x] Docker Compose modo db-only funcional ✅
- [x] Testing de integración automatizado (script `test_integration.sh`) ✅
- [x] Documentación de APIs (Swagger Java ✅, Swagger Python ✅)
- [ ] Docker Compose modo full (Python + Java + PostgreSQL) - ⏹️ Preparado, no requerido

- [ ] Deployment en producción - ⏹️ Fuera de alcance académico

## 🚀 Próximos Pasos (Opcional - Post-Entrega)

> ℹ️ **Nota:** Los requisitos académicos principales están cumplidos. Lo siguiente es opcional para extensión futura.

1. **Testing Formal:** ⏹️ (Opcional)
   - ⏹️ Tests unitarios con JUnit 5 / pytest
   - ⏹️ Tests de integración formales
   - ⏹️ Tests de repositorios JPA
   - ⏹️ Cobertura de código
   
2. **Mejoras de Integración:** ✅ (Funcionalidades core completadas)
   - ✅ Llamadas HTTP entre servicios - **FUNCIONANDO**
   - ✅ Validación JWT cross-service - **FUNCIONANDO**
   - ⏹️ Circuit breakers (Resilience4j) - Opcional
   - ⏹️ Service mesh (Istio) - Fuera de alcance
   
3. **Módulos Avanzados:** ⏹️ (Fuera de alcance académico)
   - ⏹️ Predicción ML con scikit-learn
   - ⏳ Analytics y dashboards con pandas
   - ⏳ Reportes PDF/Excel (reportlab/openpyxl)
   - ⏳ Visualizaciones con matplotlib/plotly
   
4. **Docker Compose Full Stack:** ⏳
   - ⏳ Modo full con Python + Java + PostgreSQL
   - ⏳ Networking entre contenedores
   - ⏳ Variables de entorno unificadas
   - ⏳ Health checks y dependencias
   
5. **Deployment:** ⏳
   - ⏳ CI/CD Pipeline
   - ⏳ Configuración de producción
   - ⏳ Monitoreo y logs centralizados

---

## 📂 Estructura del Repositorio

```
TP_Prog_Vanguardia/
├── README.md                       # 📄 Este archivo - Documentación completa con guía de inicio
├── LICENSE                         # ⚖️ Licencia del proyecto
├── consigna.md                     # 📋 Consigna original del trabajo
├── requirements.txt                # 📦 Dependencias Python
├── pyproject.toml                  # 🔧 Configuración de proyecto Python
├── main.py                         # 🐍 Punto de entrada de la aplicación
├── Dockerfile                      # 🐳 Configuración de contenedor Python
├── setup.sh                        # ⚡ Script de instalación automatizada
│
├── app/                            # 🏗️ Código fuente principal
│   ├── __init__.py
│   ├── api/                        # 📡 Endpoints de la API
│   │   └── v1/
│   │       ├── endpoints/          # 🔌 Controladores REST
│   │       │   ├── personas.py     # 👥 API de usuarios
│   │       │   ├── salas.py        # 🏛️ API de salas
│   │       │   ├── articulos.py    # 📦 API de artículos
│   │       │   ├── reservas.py     # 📅 API de reservas
│   │       │   └── auth.py         # 🔐 Autenticación
│   │       └── router.py           # 🗺️ Enrutador principal
│   ├── auth/                       # 🔒 Sistema de autenticación
│   │   ├── jwt_handler.py          # 🎫 Manejo de tokens JWT
│   │   └── dependencies.py         # 🔑 Dependencias de auth
│   ├── core/                       # ⚙️ Configuración central
│   │   ├── config.py               # 📋 Variables de entorno
│   │   └── database.py             # 💾 Conexión a DB
│   ├── models/                     # 🗃️ Modelos de base de datos
│   │   ├── persona.py              # 👤 Modelo de usuarios
│   │   ├── sala.py                 # 🏛️ Modelo de salas
│   │   ├── articulo.py             # 📦 Modelo de artículos
│   │   └── reserva.py              # 📅 Modelo de reservas
│   ├── schemas/                    # 📝 Esquemas Pydantic
│   │   ├── persona.py              # Validación de usuarios
│   │   ├── sala.py                 # Validación de salas
│   │   ├── articulo.py             # Validación de artículos
│   │   ├── reserva.py              # Validación de reservas
│   │   └── auth.py                 # Validación de auth
│   ├── repositories/               # 📚 Capa de acceso a datos
│   │   ├── persona_repository.py
│   │   ├── sala_repository.py
│   │   ├── articulo_repository.py
│   │   └── reserva_repository.py
│   ├── services/                   # 🔧 Lógica de negocio
│   │   ├── persona_service.py
│   │   ├── sala_service.py
│   │   ├── articulo_service.py
│   │   ├── reserva_service.py
│   │   └── auth_service.py
│   ├── web/                        # 🌐 Frontend web
│   │   └── routes.py               # Rutas de páginas HTML
│   └── prediction/                 # 🤖 Módulo ML (pendiente)
│
├── templates/                      # 🎨 Plantillas HTML
│   ├── base.html                   # Plantilla base
│   ├── login.html                  # Página de login
│   ├── dashboard.html              # Dashboard principal
│   ├── personas.html               # Gestión de usuarios
│   ├── salas.html                  # Gestión de salas
│   ├── inventario.html             # Gestión de artículos
│   └── reservas.html               # Gestión de reservas
│
├── static/                         # 📁 Archivos estáticos
│   ├── css/
│   │   └── style.css               # Estilos personalizados
│   └── js/
│       ├── auth.js                 # Gestión de autenticación
│       └── main.js                 # JavaScript principal
│
├── docker/                         # 🐳 Configuración Docker
│   ├── README.md                   # 📘 Guía completa de Docker
│   ├── .env.example                # 🔧 Plantilla de variables de entorno
│   ├── docker-compose.db-only.yml  # Solo base de datos
│   ├── docker-compose.full.yml     # Stack completo
│   ├── start-db-only.sh            # Script para modo DB-only
│   ├── start-full.sh               # Script para modo full
│   ├── stop-all.sh                 # Detener contenedores
│   └── init-scripts/
│       ├── README.md               # 🔒 Documentación de seguridad SQL
│       └── 01-init.sql             # Script de inicialización DB
│
├── java-service/                   # ☕ Microservicio Java
│   ├── README.md                   # 📗 Documentación Java service
│   ├── Dockerfile                  # 🐳 Imagen Docker Java
│   ├── pom.xml                     # 📦 Dependencias Maven
│   └── src/
│       ├── main/
│       │   ├── java/com/reservas/
│       │   │   ├── ReservasApplication.java
│       │   │   ├── controller/     # 🎮 Controladores REST
│       │   │   ├── service/        # 🔧 Servicios de negocio
│       │   │   ├── repository/     # 📚 Repositorios JPA
│       │   │   ├── model/          # 🗃️ Entidades JPA
│       │   │   ├── dto/            # 📄 Data Transfer Objects
│       │   │   ├── config/         # ⚙️ Configuraciones
│       │   │   └── exception/      # ⚠️ Manejo de excepciones
│       │   └── resources/
│       │       └── application.properties
│       └── test/                   # 🧪 Tests Java
│
├── docs/                           # 📚 Documentación técnica
│   ├── README.md                   # � Índice de documentación
│   ├── CAMBIOS_RECIENTES.md        # 📝 Detalle de últimas implementaciones
│   ├── CHECKLIST_GENERAL.md        # ✅ Verificación completa del proyecto
│   ├── RESUMEN_EJECUTIVO.md        # 📋 Resumen ejecutivo de tareas
│   ├── COMMIT_MESSAGE.md           # 💬 Mensajes de commit sugeridos
│   ├── architecture.md             # 🏛️ Arquitectura del sistema
│   ├── security.md                 # 🔐 Guía de seguridad
│   ├── formato_codigo.md           # 📝 Estándares de código
│   └── internal/                   # 🔒 Documentos internos (no en git)
│
├── scripts/                        # 🛠️ Scripts útiles
│   ├── README.md                   # 📖 Documentación de scripts
│   ├── check_code_quality.sh       # ✅ Verificación de calidad
│   ├── init_db.py                  # 💾 Inicializar base de datos
│   ├── create_admin.py             # 👤 Crear admin (SOLO desarrollo)
│   └── create_admin_secure.py      # 🔐 Crear admin (modo seguro)
│
├── postman/                        # 📮 Colecciones Postman
│   ├── README.md                   # Guía de uso
│   └── Sistema_Completo_API_Collection.postman_collection.json
│
├── tests/                          # 🧪 Tests automatizados
│   ├── unit/                       # Tests unitarios
│   └── integration/                # Tests de integración
│
└── migrations/                     # 📊 Migraciones de DB
    └── README.md
```

### 🔍 Navegación Rápida

**Para empezar:**
- 🚀 [Inicio Rápido](#-inicio-rápido) - Guía multi-plataforma (Windows/Mac/Linux)
- 🐳 [`docker/README.md`](./docker/README.md) - Usar con Docker

**Para desarrollar:**
- 🏗️ [`docs/architecture.md`](./docs/architecture.md) - Entender el diseño
- 📝 [`docs/formato_codigo.md`](./docs/formato_codigo.md) - Estándares
- ☕ [`java-service/README.md`](./java-service/README.md) - API Java
- � [`scripts/README.md`](./scripts/README.md) - Scripts y utilidades

**Para evaluar:**
- 📊 **Estado Actual del Proyecto** (ver sección en este README)
- 📝 [`docs/CAMBIOS_RECIENTES.md`](./docs/CAMBIOS_RECIENTES.md) - Últimas implementaciones
- ✅ [`docs/CHECKLIST_GENERAL.md`](./docs/CHECKLIST_GENERAL.md) - Verificación completa
- 🔐 [`docs/security.md`](./docs/security.md) - Seguridad
- 📮 [`postman/README.md`](./postman/README.md) - Testing

**Para entender la DB:**
- 💾 [`docker/init-scripts/README.md`](./docker/init-scripts/README.md) - Scripts SQL
- 📋 Schema ERD (ver [`docs/architecture.md`](./docs/architecture.md))

---

## 📈 Resumen de Lo Implementado vs Pendiente

### ✅ Implementado y Funcional
- ✅ **Python Service completo** - FastAPI + Auth JWT + CRUD + Frontend Web
- ✅ **Java Service completo** - Spring Boot + ABM Salas + ABM Artículos + Swagger
- ✅ **Integración HTTP Python ↔ Java** - ✅ **ACTIVA** 
  - Python valida salas con Java al crear reservas
  - Java valida JWT con Python al crear recursos
  - Endpoints de demostración funcionando
  - Script de testing automatizado (`test_integration.sh`)
- ✅ **Base de datos PostgreSQL** - Schema completo, datos de prueba, Docker
- ✅ **Docker infrastructure** - Modo db-only funcional, Dockerfiles listos
- ✅ **Documentación** - READMEs completos, Swagger APIs, guías de seguridad
- ✅ **Scripts de setup** - Instalación automatizada, configuración segura
- ✅ **Frontend web** - Login, dashboard, gestión de personas/salas/reservas

### ⏹️ No Requerido (Infraestructura Preparada)
- ⏹️ **Testing Formal** - Tests unitarios e integración (estructura creada, no requerido académicamente)
- ⏹️ **Docker Compose Full** - Orquestación completa (db-only funcional, full-stack preparado)
- ⏹️ **Módulos ML** - Predicción con scikit-learn (infraestructura lista, fuera de alcance)
- ⏹️ **Analytics Avanzado** - Dashboards y métricas con pandas (infraestructura lista, no requerido)
- ⏹️ **Reportes PDF/Excel** - reportlab/openpyxl (no forma parte de requisitos)
- ⏹️ **CI/CD** - Pipeline de integración continua (proyecto académico)
- ⏹️ **Deployment Producción** - Configuración cloud (fuera de alcance)

### 🎯 Funcionalidades Core Completadas
1. ✅ **Arquitectura Microservicios** - Python + Java funcionando independientemente
2. ✅ **Integración Bidireccional** - Comunicación HTTP activa entre servicios
3. ✅ **ABM Completo** - Usuarios, Salas, Artículos, Reservas
4. ✅ **Autenticación JWT** - Login, roles, validación cross-service
5. ✅ **Base de Datos Compartida** - PostgreSQL con datos de prueba
6. ✅ **Frontend Funcional** - Interfaz web completa y responsive
7. ✅ **Docker** - Containerización y orquestación básica
8. ✅ **Documentación Completa** - Guías técnicas y de usuario

## 🤝 Equipo de Desarrollo

Proyecto desarrollado como parte del trabajo práctico de **Programación de Vanguardia**

- **Institución:** Universidad De la Ciudad
- **Carrera:** Licenciatura en Tecnologías Informáticas
- **Ciclo Lectivo:** 2025

## 📄 Licencia

Este proyecto es de uso académico para la asignatura Programación de Vanguardia.

---

📧 **Contacto:** Para consultas sobre el proyecto, contactar al equipo de desarrollo.