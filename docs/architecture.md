# 🏗️ Arquitectura del Sistema de Reservas - Microservicios Python + Java

## � Visión General

Sistema de gestión de reservas implementado con arquitectura de microservicios, combinando **Python (FastAPI)** para operaciones CRUD básicas y autenticación, con **Java (Spring Boot)** para lógica de negocio avanzada, reportes y predicciones ML.

## 🌐 Arquitectura de Microservicios

```
┌─────────────────────────────────────────────────┐
│         FRONTEND WEB (React/Vue/Angular)        │
│              Templates HTML + JavaScript         │
└────────────────┬────────────────────────────────┘
                 │
                 ├──────────────────┬──────────────────┐
                 ▼                  ▼                  │
    ┌────────────────────┐  ┌────────────────────┐   │
    │  PYTHON SERVICE    │  │   JAVA SERVICE     │   │
    │  FastAPI - 8000    │  │ Spring Boot - 8080 │   │
    ├────────────────────┤  ├────────────────────┤   │
    │ 👤 ABM Usuarios    │  │ 🏢 ABM Salas       │   │
    │ � Sistema Reservas│  │ �📦 ABM Artículos   │   │
    │ 🔐 Autenticación   │  │                    │   │
    │ 🤖 Predicción ML   │  │                    │   │
    │ � Analytics       │  │                    │   │
    │ � Reportes        │  │                    │   │
    └────────┬───────────┘  └────────┬───────────┘   │
             │                       │               │
             └───────────┬───────────┘               │
                         ▼                           │
                ┌─────────────────┐                  │
                │   PostgreSQL    │                  │
                │   Port 5432     │◄─────────────────┘
                ├─────────────────┤
                │ • Personas      │
                │ • Salas         │
                │ • Articulos     │
                │ • Reservas      │
                │ • Analytics     │
                └─────────────────┘
```

## 🐍 Python Service (FastAPI - Port 8000)

### Responsabilidades
- **Gestión de Usuarios (Personas)**: CRUD completo con autenticación JWT
- **Sistema de Reservas**: Creación, modificación y consulta de reservas
- **Autenticación y Autorización**: JWT tokens, roles (admin/usuario)
- **Frontend Web**: Servir templates HTML y archivos estáticos
- **Predicción ML**: Modelos de machine learning para predicción de demanda (scikit-learn, pandas, numpy)
- **Analytics**: Análisis de datos, estadísticas y patrones de uso
- **Reportes Avanzados**: Generación de informes complejos en PDF/Excel

### Estructura del Proyecto Python

```
python-service/
├── app/
│   ├── api/v1/
│   │   ├── endpoints/
│   │   │   ├── personas.py      # ABM Usuarios + Auth
│   │   │   ├── reservas.py      # Sistema Reservas
│   │   │   ├── analytics.py     # Analytics y métricas
│   │   │   ├── reportes.py      # Reportes avanzados
│   │   │   └── demo.py          # Endpoints de prueba
│   │   └── router.py
│   ├── auth/                     # Autenticación JWT
│   ├── core/
│   │   ├── config.py            # Configuración
│   │   └── database.py          # Conexión PostgreSQL
│   ├── models/                   # SQLAlchemy Models
│   │   ├── persona.py
│   │   ├── sala.py
│   │   └── reserva.py
│   ├── repositories/             # Patrón Repository
│   ├── schemas/                  # Pydantic Schemas
│   ├── services/                 # Lógica de negocio
│   └── prediction/               # Machine Learning
│       ├── models/               # Modelos ML
│       ├── data_processor.py    # Procesamiento de datos
│       └── predictor.py         # Motor de predicción
├── templates/                    # Jinja2 Templates
├── static/                       # CSS, JS, assets
└── main.py                       # Aplicación FastAPI
```

### Endpoints Python (Port 8000)

#### Autenticación
- `POST /api/v1/personas/login` - Login con JWT
- `POST /api/v1/personas/web-login` - Login con cookies
- `POST /api/v1/personas/logout` - Cerrar sesión
- `GET /api/v1/personas/me` - Usuario actual

#### Personas
- `GET /api/v1/personas` - Listar usuarios
- `POST /api/v1/personas` - Crear usuario
- `GET /api/v1/personas/{id}` - Obtener usuario
- `PUT /api/v1/personas/{id}` - Actualizar usuario
- `DELETE /api/v1/personas/{id}` - Eliminar usuario

#### Reservas
- `GET /api/v1/reservas` - Listar reservas
- `POST /api/v1/reservas` - Crear reserva
- `GET /api/v1/reservas/{id}` - Obtener reserva
- `PUT /api/v1/reservas/{id}` - Actualizar reserva
- `DELETE /api/v1/reservas/{id}` - Eliminar reserva

#### Analytics (Propuesto)
- `GET /api/v1/analytics/usage-patterns` - Patrones de uso
- `GET /api/v1/analytics/trends` - Tendencias temporales
- `GET /api/v1/analytics/dashboard` - Métricas del dashboard
- `GET /api/v1/analytics/heatmap` - Mapa de calor de reservas
- `GET /api/v1/analytics/statistics` - Estadísticas generales

#### Reportes (Propuesto)
- `GET /api/v1/reportes/reservas-por-periodo` - Reporte por período
- `GET /api/v1/reportes/recursos-mas-usados` - Recursos populares
- `GET /api/v1/reportes/utilizacion` - Utilización de recursos
- `POST /api/v1/reportes/custom` - Reporte personalizado
- `GET /api/v1/reportes/export/{formato}` - Exportar (PDF, Excel)

#### Predicción ML (Propuesto)
- `GET /api/v1/prediction/demand/{resourceId}` - Predecir demanda
- `GET /api/v1/prediction/peak-hours` - Horarios pico predichos
- `GET /api/v1/prediction/optimal-allocation` - Optimización de recursos
- `POST /api/v1/prediction/train` - Entrenar modelo
- `GET /api/v1/prediction/accuracy` - Métricas del modelo

### Tecnologías Python
- **FastAPI** - Framework web moderno
- **SQLAlchemy 2.0** - ORM con Mapped types
- **Pydantic** - Validación y serialización
- **JWT** - Autenticación con tokens
- **Jinja2** - Motor de templates
- **PostgreSQL** - Base de datos
- **scikit-learn** - Machine Learning
- **pandas** - Análisis de datos
- **numpy** - Computación numérica
- **matplotlib/plotly** - Visualización de datos
- **reportlab** - Generación de PDFs
- **Jinja2** - Motor de templates
- **PostgreSQL** - Base de datos

## ☕ Java Service (Spring Boot - Port 8080)

### Responsabilidades
- **Gestión de Salas**: CRUD de espacios reservables (migrado desde Python)
- **Gestión de Artículos**: CRUD de recursos e inventario

### Estructura del Proyecto Java (Propuesta)

```
java-service/
├── src/main/java/com/reservas/
│   ├── controller/
│   │   ├── SalaController.java
│   │   └── ArticuloController.java
│   ├── service/
│   │   ├── SalaService.java
│   │   └── ArticuloService.java
│   ├── repository/
│   │   ├── SalaRepository.java
│   │   └── ArticuloRepository.java
│   ├── model/
│   │   ├── Sala.java
│   │   ├── Articulo.java
│   │   └── dto/
│   └── config/
│       ├── DatabaseConfig.java
│       └── CorsConfig.java
├── src/main/resources/
│   └── application.properties
└── pom.xml
```

### Endpoints Java (Port 8080) - Propuestos

#### Salas
- `GET /api/salas` - Listar salas
- `POST /api/salas` - Crear sala
- `GET /api/salas/{id}` - Obtener sala
- `PUT /api/salas/{id}` - Actualizar sala
- `DELETE /api/salas/{id}` - Eliminar sala
- `GET /api/salas/disponibles` - Salas disponibles

#### Artículos
- `GET /api/articulos` - Listar artículos
- `POST /api/articulos` - Crear artículo
- `GET /api/articulos/{id}` - Obtener artículo
- `PUT /api/articulos/{id}` - Actualizar artículo
- `DELETE /api/articulos/{id}` - Eliminar artículo
- `GET /api/articulos/disponibles` - Artículos disponibles
- `GET /api/articulos/categoria/{categoria}` - Filtrar por categoría

### Tecnologías Java
- **Spring Boot 3.x** - Framework principal
- **Spring Data JPA** - ORM y repositorios
- **PostgreSQL Driver** - Conexión a base de datos
- **Lombok** - Reducción de boilerplate
- **JUnit 5** - Testing
- **Maven** - Gestión de dependencias

## 🗄️ Base de Datos PostgreSQL (Port 5432)

### Tablas Principales

#### personas
```sql
- id: SERIAL PRIMARY KEY
- nombre: VARCHAR(255)
- email: VARCHAR(255) UNIQUE
- password_hash: VARCHAR(255)
- is_admin: BOOLEAN
- created_at: TIMESTAMP
```

#### salas
```sql
- id: SERIAL PRIMARY KEY
- nombre: VARCHAR(255)
- capacidad: INTEGER
- disponible: BOOLEAN
```

#### articulos
```sql
- id: SERIAL PRIMARY KEY
- nombre: VARCHAR(255)
- disponible: BOOLEAN
- categoria: VARCHAR(100)
- descripcion: TEXT
```

#### reservas
```sql
- id: SERIAL PRIMARY KEY
- id_articulo: INTEGER (FK → articulos)
- id_sala: INTEGER (FK → salas)
- id_persona: INTEGER (FK → personas)
- fecha_hora_inicio: TIMESTAMP
- fecha_hora_fin: TIMESTAMP
- estado: VARCHAR(50)
```

#### analytics (tabla adicional para ML)
```sql
- id: SERIAL PRIMARY KEY
- fecha: DATE
- recurso_tipo: VARCHAR(50)
- recurso_id: INTEGER
- total_reservas: INTEGER
- horas_uso: DECIMAL
- tasa_ocupacion: DECIMAL
```

## 🔄 Comunicación entre Servicios

### Python → Java
```python
import httpx

# Desde Python llamar a Java para predicciones
async def get_demand_prediction(articulo_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://localhost:8080/api/prediction/demand/{articulo_id}"
        )
        return response.json()
```

### Java → Python
```java
// Desde Java llamar a Python para validar usuario
@Service
public class PythonAuthClient {
    @Value("${python.service.url}")
    private String pythonUrl;
    
    public boolean validateUser(String token) {
        RestTemplate restTemplate = new RestTemplate();
        String url = pythonUrl + "/api/v1/personas/me";
        // ... validación
    }
}
```

### Compartir Base de Datos
Ambos servicios acceden a PostgreSQL:
- **Python**: Lectura/Escritura en personas, salas, reservas
- **Java**: Lectura/Escritura en articulos, analytics; Solo lectura en reservas

## 🏛️ Patrones de Arquitectura

### Patrón Repository (Ambos servicios)
Abstracción del acceso a datos:
```
Controller/Endpoint → Service → Repository → Database
```

### Domain-Driven Design
- **Entities**: Modelos de dominio (Persona, Sala, Articulo, Reserva)
- **Services**: Lógica de negocio encapsulada
- **Repositories**: Persistencia abstracta

### API Gateway (Futuro)
Considerar implementar un API Gateway (NGINX, Kong) para:
- Routing unificado
- Autenticación centralizada
- Rate limiting
- Load balancing

## 🔐 Seguridad

### Autenticación
- **Python**: JWT tokens con cookies HTTP-only
- **Java**: Validación de tokens JWT del servicio Python

### Autorización
- Roles: `admin` y `usuario`
- Python maneja autenticación principal
- Java valida tokens antes de operaciones sensibles

### CORS
Configurado en ambos servicios para permitir:
- Frontend en diferentes puertos
- Comunicación inter-servicios

## 🚀 Despliegue

### Desarrollo Local
```bash
# Python Service
cd python-service
python main.py
# → http://localhost:8000

# Java Service
cd java-service
./mvnw spring-boot:run
# → http://localhost:8080

# PostgreSQL
docker-compose up postgres
# → localhost:5432
```

### Docker Compose (Propuesto)
```yaml
services:
  postgres:
    image: postgres:15
    ports: ["5432:5432"]
  
  python-service:
    build: ./python-service
    ports: ["8000:8000"]
    depends_on: [postgres]
  
  java-service:
    build: ./java-service
    ports: ["8080:8080"]
    depends_on: [postgres]
  
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
```

## 📊 Flujo de Datos

### Crear Reserva con Predicción
1. Usuario crea reserva en Frontend
2. Frontend → Python `/api/v1/reservas` (POST)
3. Python valida usuario y disponibilidad
4. Python → Java `/api/prediction/demand/{recurso_id}` (GET)
5. Java analiza patrones y retorna predicción
6. Python crea reserva en BD
7. Python retorna confirmación al Frontend

### Generar Reporte
1. Admin solicita reporte en Frontend
2. Frontend → Java `/api/reportes/reservas-por-periodo` (GET)
3. Java consulta datos de PostgreSQL (tablas: reservas, articulos, salas)
4. Java procesa y genera reporte
5. Java retorna PDF/JSON al Frontend

## 🧪 Testing

### Python
- **pytest** - Unit tests
- **httpx** - Integration tests
- **coverage** - Code coverage

### Java
- **JUnit 5** - Unit tests
- **MockMvc** - Controller tests
- **Testcontainers** - Integration tests con PostgreSQL

## 📈 Escalabilidad Futura

1. **API Gateway**: NGINX o Kong para routing
2. **Cache**: Redis para sesiones y datos frecuentes
3. **Message Queue**: RabbitMQ/Kafka para comunicación asíncrona
4. **Containerización**: Docker + Kubernetes
5. **Monitoring**: Prometheus + Grafana