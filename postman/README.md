# Colección de Postman para Sistema de Reservas

Este directorio contiene la colección completa de Postman para testear todos los endpoints de la API del Sistema de Reservas de Salas.

## 📁 Archivos Incluidos

### **Sistema_Completo_API_Collection.postman_collection.json** ⭐
**Colección consolidada que incluye TODAS las funcionalidades del sistema**

- **Organización por carpetas**:
  - 🏥 **Sistema - Health & Configuration**: Verificación de estado y configuración
  - 👥 **Personas - CRUD Completo**: Gestión completa de personas
  - 🏛️ **Salas - Gestión Completa**: Administración de salas y espacios
  - 📦 **Artículos - Inventario Completo**: Gestión del inventario de equipamiento
  - 📅 **Reservas - Sistema Completo**: Sistema de reservas con casos avanzados  
  - 🔬 **Testing Avanzado y QA**: Performance, seguridad y casos edge
  - ⚠️ **Manejo de Errores**: Validación de errores y casos límite

- **Características**:
  - ✅ Una sola colección para todo el sistema
  - ✅ Navegación organizada por módulos
  - ✅ Variables compartidas entre módulos
  - ✅ Testing completo en un solo archivo
  - ✅ Fácil importación y mantenimiento
  - ✅ +100 requests organizados por funcionalidad
  - ✅ Tests automatizados integrados

## Configuración

### Variables de Entorno Requeridas

Crear un entorno en Postman con las siguientes variables:

```json
{
  "base_url": "http://localhost:8000",
  "docente_id": "1",
  "estudiante_id": "2", 
  "sala_conferencias_id": "1",
  "proyector_id": "1",
  "reserva_id": "1"
}
```

### Variables Dinámicas (Auto-generadas)

Las colecciones establecen automáticamente:
- `{{docente_id}}` - ID del docente creado
- `{{estudiante_id}}` - ID del estudiante creado
- `{{sala_conferencias_id}}` - ID de sala de conferencias
- `{{proyector_id}}` - ID del proyector creado
- `{{reserva_id}}` - ID de reserva creada

## 📋 Orden de Ejecución Recomendado

### **Flujo Completo de Testing:**
1. **🏥 Sistema - Health & Configuration** - Verificar conectividad
2. **👥 Personas - CRUD Completo** - Crear usuarios base
3. **🏛️ Salas - Gestión Completa** - Configurar espacios
4. **📦 Artículos - Inventario Completo** - Poblar inventario
5. **📅 Reservas - Sistema Completo** - Testing de reservas
6. **🔬 Testing Avanzado y QA** - Validación avanzada
7. **⚠️ Manejo de Errores** - Testing de casos límite

### **Testing Modular:**
Puedes ejecutar carpetas individuales según tus necesidades:
- Para **desarrollo**: Ejecuta solo las carpetas del módulo en el que trabajas
- Para **integración**: Ejecuta carpetas 1-5 en orden
- Para **QA completo**: Ejecuta todas las carpetas en orden

## 🎯 Casos de Uso Incluidos

### Scenarios Básicos:
- ✅ CRUD completo para todos los recursos
- ✅ Validación de datos de entrada
- ✅ Manejo de errores estándar
- ✅ Paginación y filtros

### Scenarios Avanzados:
- 🔄 Flujos de trabajo completos de reservas
- 📊 Testing de performance y carga
- 🛡️ Validación de seguridad (SQL injection, XSS)
- ⚡ Casos edge y límites del sistema
- 🔍 Testing de concurrencia
- 🧪 Stress testing con datos extremos

## 🔧 Scripts de Testing Incluidos

Cada colección incluye:
- **Pre-request Scripts**: Configuración automática de variables
- **Tests**: Validación automática de respuestas
- **Assertions**: Verificación de estructura de datos
- **Performance Checks**: Medición de tiempos de respuesta
- **Security Tests**: Validación de protecciones de seguridad

## 🚀 Ejecución por CLI

```bash
# Instalar Newman
npm install -g newman

# Ejecutar colección consolidada
newman run Sistema_Completo_API_Collection.postman_collection.json -e environment.json

# Ejecutar con reporte HTML
newman run Sistema_Completo_API_Collection.postman_collection.json -e environment.json --reporters cli,html --reporter-html-export report.html

# Ejecutar solo una carpeta específica
newman run Sistema_Completo_API_Collection.postman_collection.json -e environment.json --folder "Personas - CRUD Completo"
```

## 📄 Notas Técnicas

- ✅ Optimizado para **FastAPI**
- ✅ Compatible con **Swagger/OpenAPI** endpoints
- ✅ Incluye ejemplos realistas de datos universitarios
- ✅ Tests automáticos con **Chai assertions**
- ✅ Soporte completo para **Newman** (CLI runner)
- ✅ Variables de entorno compartidas entre módulos
- ✅ Testing de seguridad integrado

## 🔄 Mantenimiento

- **Archivo único**: Actualizar solo `Sistema_Completo_API_Collection.postman_collection.json`
- **Nuevos endpoints**: Agregar en la carpeta correspondiente
- **Variables**: Mantener actualizadas según cambios en la API
- **Testing**: Revisar y actualizar casos regularmente
- **Documentación**: Actualizar este README cuando agregues funcionalidades

## 🚀 Cómo Importar en Postman

1. Abrir Postman
2. Hacer clic en **Import**
3. Arrastrar el archivo `Sistema_Completo_API_Collection.postman_collection.json`
4. Crear un **Environment** con las variables listadas arriba
5. ¡Comenzar a testear!

## 📊 Métricas y Reportes

La colección consolidada incluye:
- ⏱️ Medición de tiempos de respuesta
- 📈 Contadores de éxito/fallo por módulo
- 🔍 Logging detallado para debugging
- 📋 Reportes automáticos de cobertura