# Arquitectura del Proyecto

```
TP_Prog_Vanguardia/
├── app/                          # Código principal de la aplicación
│   ├── api/                      # Capa de API REST
│   │   └── v1/                   # Versionado de API
│   │       └── endpoints/        # Endpoints REST por recurso
│   ├── auth/                     # Autenticación y autorización
│   ├── core/                     # Configuración central
│   ├── models/                   # Modelos de base de datos (SQLAlchemy)
│   ├── prediction/               # Módulo de predicción de reservas
│   ├── repositories/             # Capa de acceso a datos (Repository Pattern)
│   ├── schemas/                  # Esquemas Pydantic para validación
│   └── services/                 # Lógica de negocio
├── config/                       # Configuraciones por ambiente
├── docs/                         # Documentación del proyecto
├── migrations/                   # Migraciones de base de datos
└── tests/                        # Pruebas automatizadas
    ├── integration/              # Pruebas de integración
    └── unit/                     # Pruebas unitarias
```

## Principios de Diseño Aplicados

### Clean Architecture
- **Separación de responsabilidades** por capas
- **Inversión de dependencias** con repositories
- **Independencia de frameworks** en la lógica de negocio

### REST API Design
- **Versionado de API** (/api/v1/)
- **Recursos bien definidos** por endpoint
- **Métodos HTTP semánticamente correctos**

### Domain-Driven Design
- **Modelos** representan entidades del dominio
- **Servicios** contienen lógica de negocio
- **Repositories** abstraen el acceso a datos