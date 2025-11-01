# 📚 Documentación del Proyecto

**Sistema de Reservas con Arquitectura de Microservicios**
**Última actualización:** 16 de octubre de 2025

---

## 🗂️ Índice de Documentación

### 📖 Documentación Principal

| Documento | Descripción | Para quién |
|-----------|-------------|------------|
| **[architecture.md](./architecture.md)** | Arquitectura técnica completa del sistema | 🧑‍💻 Desarrolladores |
| **[INTEGRACION.md](./INTEGRACION.md)** | Guía completa de integración Python ↔ Java | 🧑‍💻 Desarrolladores |
| **[security.md](./security.md)** | Guía de seguridad y mejores prácticas | 🔐 DevOps/Security |
| **[formato_codigo.md](./formato_codigo.md)** | Estándares de código y convenciones | 🧑‍💻 Desarrolladores |

### 📊 Estado del Proyecto

| Documento | Descripción | Ubicación |
|-----------|-------------|-----------|
| **[README.md - Estado Actual](../README.md#-estado-actual-del-proyecto)** | Estado general y progreso del proyecto | 📄 README principal |
| **[CAMBIOS_RECIENTES.md](./CAMBIOS_RECIENTES.md)** | Últimas implementaciones y correcciones | 📚 /docs |

### 📁 Documentación Interna (No Versionada)

Los siguientes documentos están en **`docs/internal/`** (carpeta local, no en GitHub):
- Borradores y análisis de trabajo
- Historial detallado de cambios
- Documentos de proceso interno
- Ver **[internal/README.md](./internal/README.md)** para más detalles

> 💡 Estos archivos sirven como **banco de memoria** pero no se suben a GitHub para mantener el repositorio limpio.

---

## 🎯 Guía Rápida por Perfil

### 👨‍💻 Si eres Desarrollador
1. Lee **[architecture.md](./architecture.md)** para entender la arquitectura
2. Consulta **[INTEGRACION.md](./INTEGRACION.md)** para trabajar con la integración
3. Sigue **[formato_codigo.md](./formato_codigo.md)** para mantener estándares
4. Revisa **[security.md](./security.md)** antes de hacer cambios

### 🎓 Si eres Evaluador/Profesor
1. Lee la sección **[Estado Actual del Proyecto](../README.md#-estado-actual-del-proyecto)** en el README principal
2. Revisa **[architecture.md](./architecture.md)** para arquitectura técnica completa
3. Consulta **[INTEGRACION.md](./INTEGRACION.md)** para entender la integración Python ↔ Java
4. Prueba las funcionalidades con la **[guía de integración](./INTEGRACION.md)**

### 🚀 Si eres Usuario/Tester
1. Ve al **[README principal](../README.md)** para instrucciones de instalación
2. Usa **[INTEGRACION.md](./INTEGRACION.md)** para probar funcionalidades
3. Consulta **[architecture.md](./architecture.md)** para entender el sistema

---

## 📊 Estado Actual del Proyecto

### ✅ Componentes Funcionales (75% completado)

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

### 🎯 Funcionalidades Core Implementadas

#### Python Service (Port 8000)
- ✅ ABM Usuarios con roles (admin/usuario)
- ✅ Autenticación JWT completa
- ✅ Sistema de Reservas **con integración Java**
- ✅ Frontend web completo y responsive
- ✅ API REST documentada (Swagger)
- ✅ Cliente HTTP para Java Service

#### Java Service (Port 8080)
- ✅ ABM Salas (8 endpoints REST)
- ✅ ABM Artículos (8 endpoints REST)
- ✅ Validación JWT **con integración Python**
- ✅ API REST documentada (Swagger)
- ✅ Cliente HTTP para Python Service

#### Integración Python ↔ Java
- ✅ **Python valida salas con Java** al crear reservas
- ✅ **Java valida JWT con Python** al crear recursos
- ✅ Fallback automático si un servicio no responde
- ✅ 5 endpoints de demostración
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
┌──────────────────────┐
│   Frontend Web       │
│   (Templates + JS)   │
└──────────┬───────────┘
           │ HTTP/REST
           ▼
┌──────────────────────┐ 🔗 HTTP ┌──────────────────────┐
│   PYTHON SERVICE     │◄───────►│   JAVA SERVICE       │
│   FastAPI : 8000     │         │   Spring Boot : 8080 │
├──────────────────────┤         ├──────────────────────┤
│ • Auth JWT           │         │ • ABM Salas          │
│ • ABM Usuarios       │─valida─→│ • ABM Artículos      │
│ • Reservas           │  salas  │ • Valida JWT         │
│ • Frontend Web       │         │ • Swagger            │
└──────────┬───────────┘         └──────────┬───────────┘
           │                                 │
           │      PostgreSQL Compartida      │
           └────────────┬────────────────────┘
                        ▼
                ┌───────────────┐
                │  PostgreSQL   │
                │  Port 5432    │
                └───────────────┘
```

**Flujo de Integración Activo:**
1. Usuario crea reserva en frontend → POST a Python
2. Python valida sala con Java → GET a Java
3. Java responde con datos de sala
4. Python crea reserva en DB
5. ✅ Reserva creada con validación cross-service

---

## 🔗 Enlaces Rápidos

### Documentación Técnica
- [Arquitectura Completa](./architecture.md)
- [Integración Python-Java](./INTEGRACION.md)
- [Seguridad](./security.md)
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

## 🧹 Archivos Temporales

Los siguientes archivos pueden ser ignorados o eliminados:

- `architecture.md.backup` - Backup del architecture.md anterior
- `architecture.md.bak` - Backup duplicado
- `architecture.md.new` - Archivo temporal de edición

---

## 📝 Cómo Usar Esta Documentación

### Para empezar desde cero:
1. Lee el **[README principal](../README.md)**
2. Configura el entorno con **[Docker README](../docker/README.md)**
3. Revisa la **[arquitectura](./architecture.md)**
4. Prueba la **[integración](./INTEGRACION.md)**

### Para entender cambios recientes:
1. **[RESUMEN_EJECUTIVO.md](./RESUMEN_EJECUTIVO.md)** - Qué se hizo
2. **[CAMBIOS_RECIENTES.md](./CAMBIOS_RECIENTES.md)** - Archivos modificados
3. **[README - Estado Actual](../README.md#-estado-actual-del-proyecto)** - Estado general del proyecto

### Para desarrollar:
1. **[formato_codigo.md](./formato_codigo.md)** - Estándares
2. **[security.md](./security.md)** - Buenas prácticas
3. **[architecture.md](./architecture.md)** - Arquitectura
4. **[INTEGRACION.md](./INTEGRACION.md)** - Cómo usar la integración

---

## 🤝 Contribuir

Si necesitas actualizar la documentación:

1. **Para cambios arquitectónicos:** Actualiza `architecture.md`
2. **Para nuevas funcionalidades:** Actualiza la sección "Estado Actual" en el README principal
3. **Para seguridad:** Actualiza `security.md`
4. **Para integración:** Actualiza `INTEGRACION.md`

---

## 📧 Soporte

- **Dudas de arquitectura:** Ver [architecture.md](./architecture.md)
- **Problemas de integración:** Ver [INTEGRACION.md](./INTEGRACION.md)
- **Issues de seguridad:** Ver [security.md](./security.md)
- **Instalación:** Ver [README principal](../README.md)

---

**Estado de Documentación:** ✅ Actualizada y organizada
**Última revisión:** 16 de octubre de 2025
**Versión:** 2.0 - Con integración HTTP documentada
