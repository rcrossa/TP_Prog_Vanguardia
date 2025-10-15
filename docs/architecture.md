# 🏗️ Arquitectura del Sistema de Reservas

## 📁 Estructura del Proyecto

```
TP_Prog_Vanguardia/
├── app/                          # Aplicación principal
│   ├── api/                      # Capa de API REST
│   │   └── v1/                   # Versionado de API
│   │       ├── endpoints/        # Endpoints por recurso
│   │       └── router.py         # Router principal
│   ├── core/                     # Configuración central
│   │   ├── config.py            # Configuración con variables de entorno
│   │   └── database.py          # Configuración de base de datos
│   ├── models/                   # Modelos SQLAlchemy 2.0
│   │   ├── persona.py           # Modelo de usuarios
│   │   ├── sala.py              # Modelo de salas
│   │   ├── articulo.py          # Modelo de artículos
│   │   └── reserva.py           # Modelo de reservas
│   ├── repositories/             # Capa de acceso a datos
│   ├── schemas/                  # Esquemas Pydantic para validación
│   └── services/                 # Lógica de negocio
├── docker/                       # Configuración de contenedores
├── docs/                         # Documentación
├── postman/                      # Colección de API testing
└── scripts/                      # Scripts de utilidad
```

## 🏛️ Patrón de Arquitectura

### Arquitectura por Capas

**API Layer (Endpoints)**
- `app/api/v1/endpoints/` - Controladores REST
- Manejo de requests/responses
- Validación de entrada con Pydantic

**Service Layer (Lógica de Negocio)**
- `app/services/` - Reglas de negocio
- Validaciones complejas
- Coordinación entre repositorios

**Repository Layer (Acceso a Datos)**
- `app/repositories/` - Patrón Repository
- Abstracción de la base de datos
- Operaciones CRUD encapsuladas

**Model Layer (Persistencia)**
- `app/models/` - Modelos SQLAlchemy 2.0
- Mapeo objeto-relacional
- Definición de esquema de BD

### Tecnologías Principales

- **FastAPI** - Framework web moderno
- **SQLAlchemy 2.0** - ORM con Mapped types
- **Pydantic** - Validación y serialización
- **PostgreSQL** - Base de datos relacional
- **Docker** - Containerización

### Domain-Driven Design
- **Modelos** representan entidades del dominio
- **Servicios** contienen lógica de negocio
- **Repositories** abstraen el acceso a datos