# 📚 Documentación del Proyecto

**Sistema de Reservas con Arquitectura de Microservicios**
**Última actualización:** 1 de noviembre de 2025

---

## 🆕 **NUEVO**: Sistema de Predicciones Implementado

📖 **Ver documentación completa**: [RESUMEN_PREDICCIONES.md](./RESUMEN_PREDICCIONES.md)

✅ **Sistema 100% funcional** con predicciones de demanda, horarios pico, detección de anomalías y recomendaciones de capacidad.

---

## 🗂️ Índice de Documentación

### 📖 Documentación Principal

| Documento | Descripción | Para quién |
|-----------|-------------|------------|
| **[architecture.md](./architecture.md)** | Arquitectura técnica completa del sistema | 🧑‍💻 Desarrolladores |
| **[configuracion_entorno.md](./configuracion_entorno.md)** | 🆕 Variables de entorno y configuración detallada | 🧑‍💻 Desarrolladores |
| **[testing.md](./testing.md)** | 🧪 **NUEVO**: Documentación de tests unitarios y SonarQube | 🧑‍💻 Desarrolladores |
| **[formato_codigo.md](./formato_codigo.md)** | Estándares de código y convenciones | 🧑‍💻 Desarrolladores |

### 🔮 **NUEVO**: Documentación de Predicciones

| Documento | Descripción | Para quién |
|-----------|-------------|------------|
| **[RESUMEN_PREDICCIONES.md](./RESUMEN_PREDICCIONES.md)** | ⭐ Resumen completo y guía de uso del sistema de predicciones | 👥 Todos |
| **[prediction_module.md](./prediction_module.md)** | Documentación técnica detallada | 🧑‍💻 Desarrolladores |
| **[ARQUITECTURA_PREDICCIONES.md](./ARQUITECTURA_PREDICCIONES.md)** | Diagramas y flujos de datos | 🏗️ Arquitectos |
| **[IMPLEMENTACION_PREDICCIONES.md](./IMPLEMENTACION_PREDICCIONES.md)** | Guía de implementación paso a paso | 🧑‍💻 Desarrolladores |

---

### 📊 Estado del Proyecto

| Documento | Descripción | Ubicación |
|-----------|-------------|-----------|
| **[README.md - Estado Actual](../README.md#-estado-actual-del-proyecto)** | Estado general y progreso del proyecto | 📄 README principal 
---

## 🎯 Guía Rápida por Perfil

### 👨‍💻 Si eres Desarrollador
1. Lee **[architecture.md](./architecture.md)** para entender la arquitectura
3. Sigue **[formato_codigo.md](./formato_codigo.md)** para mantener estándares

### 🎓 Si eres Evaluador/Profesor
1. Lee la sección **[Estado Actual del Proyecto](../README.md#-estado-actual-del-proyecto)** en el README principal
2. Revisa **[architecture.md](./architecture.md)** para arquitectura técnica completa

### 🚀 Si eres Usuario/Tester
1. Ve al **[README principal](../README.md)** para instrucciones de instalación
3. Consulta **[architecture.md](./architecture.md)** para entender el sistema

---

## 📊 Estado Actual del Proyecto

### ✅ Componentes Funcionales (~80% completado)

| Componente | Estado | Progreso |
|------------|--------|----------|
| 🐍 **Python Service** | ✅ Funcional | 100% |
| ☕ **Java Service** | ✅ Funcional | 100% |
| 🔗 **Integración HTTP** | ✅ **ACTIVA** | 100% |
| 🗄️ **PostgreSQL** | ✅ Funcional | 100% |
| 🎨 **Frontend Web** | ✅ Funcional | 100% |
| 🐳 **Docker** | ✅ Funcional | 100% |
| 📚 **Swagger/Docs** | ✅ Funcional | 100% |
| 🔐 **Autenticación JWT** | ✅ Funcional | 100% |
| 🤖 **Predicciones** | ✅ Funcional  | 100% |
| 📈 **Analytics** | ✅ Funcional  | 100% |

### 🎯 Funcionalidades Core Implementadas

#### Python Service (Port 8000)
- ✅ ABM Usuarios con roles (admin/usuario)
- ✅ Autenticación JWT completa
- ✅ Sistema de Reservas **con integración Java** (salas y artículos)
- ✅ Frontend web completo y responsive (Salas, Inventario, Reservas, Personas)
- ✅ **Sistema de Predicciones ML** (demanda, horarios pico, anomalías, capacidad)
- ✅ **Dashboard de Analytics** (métricas en tiempo real, heatmaps, KPIs)
- ✅ API REST documentada (Swagger)
- ✅ Cliente HTTP para Java Service (salas y artículos)

#### Java Service (Port 8080)
- ✅ ABM Salas (8 endpoints REST)
- ✅ ABM Artículos/Inventario (8 endpoints REST)
- ✅ Gestión de stock en tiempo real (considera solo reservas futuras)
- ✅ Validación JWT **con integración Python**
- ✅ API REST documentada (Swagger)
- ✅ Cliente HTTP para Python Service

#### Integración Python ↔ Java
- ✅ **Python valida salas con Java** al crear reservas
- ✅ **Python valida artículos/stock con Java** al crear reservas
- ✅ **Java valida JWT con Python** al crear/modificar recursos
- ✅ Fallback automático si un servicio no responde
- ✅ Endpoints de demostración de integración
- ✅ Script de testing automatizado

### 🎓 Funcionalidades NO Implementadas (No Requeridas)

Estas funcionalidades aparecen como "pendientes" en algunos documentos antiguos pero **NO eran parte de los requisitos originales** del trabajo:

- ⏹️ Machine Learning / Predicción
- ⏹️ Analytics avanzado
- ⏹️ Reportes PDF/Excel
- ⏹️ Tests unitarios formales

**Nota:** El proyecto cumple con los requisitos académicos establecidos (~75% de implementación esperada).

---

## 🏗️ Arquitectura Resumida

```
┌──────────────────────────────────┐
│      Frontend Web                │
│  (Templates + JS + Bootstrap)    │
│  Salas | Inventario | Reservas   │
└──────────────┬───────────────────┘
               │ HTTP/REST
               ▼
┌──────────────────────┐ 🔗 HTTP ┌──────────────────────┐
│   PYTHON SERVICE     │◄───────►│   JAVA SERVICE       │
│   FastAPI : 8000     │         │   Spring Boot : 8080 │
├──────────────────────┤         ├──────────────────────┤
│ • Auth JWT           │         │ • ABM Salas (8 ep)   │
│ • ABM Usuarios       │─valida─→│ • ABM Artículos (8)  │
│ • Reservas           │ salas & │ • Stock en tiempo    │
│ • Predicciones ML    │ artíc.  │   real               │
│ • Analytics          │         │ • Valida JWT         │
│ • Frontend Web       │◄─JWT────│ • Swagger            │
└──────────┬───────────┘         └──────────┬───────────┘
           │                                 │
           │      PostgreSQL Compartida      │
           └────────────┬────────────────────┘
                        ▼
                ┌───────────────┐
                │  PostgreSQL   │
                │  Port 5432    │
                ├───────────────┤
                │ • personas    │
                │ • salas       │
                │ • articulos   │
                │ • reservas    │
                └───────────────┘
```

**Flujo de Integración Activo:**
1. Usuario crea reserva en frontend → POST a Python
2. Python valida sala/artículo con Java → GET a Java
3. Java responde con datos de sala y stock disponible
4. Python verifica disponibilidad horaria
5. Python crea reserva en DB
6. Reserva creada con validación cross-service

---

## 🔗 Enlaces Rápidos

### Documentación Técnica
- [Arquitectura Completa](./architecture.md)
- [Estándares de Código](./formato_codigo.md)

### APIs y Servicios
- **Python Swagger:** http://localhost:8000/docs
- **Java Swagger:** http://localhost:8080/swagger-ui.html
- **Frontend Web:** http://localhost:8000

### Repositorio
- [README Principal](../README.md)
- [Docker README](../docker/README.md)
- [Java Service README](../java-service/README.md)
- [Postman Collection](../postman/README.md)


---

## 📝 Cómo Usar Esta Documentación

### Para empezar desde cero:
1. Lee el **[README principal](../README.md)**
2. Configura el entorno con **[Docker README](../docker/README.md)**
3. Revisa la **[arquitectura](./architecture.md)**


### Para desarrollar:
1. **[formato_codigo.md](./formato_codigo.md)** - Estándares
2. **[architecture.md](./architecture.md)** - Arquitectura

---

## 🤝 Contribuir

Si necesitas actualizar la documentación:

1. **Para cambios arquitectónicos:** Actualiza `architecture.md`
2. **Para nuevas funcionalidades:** Actualiza la sección "Estado Actual" en el README principal

---

## 📧 Soporte

- **Dudas de arquitectura:** Ver [architecture.md](./architecture.md)
- **Instalación:** Ver [README principal](../README.md)

---

