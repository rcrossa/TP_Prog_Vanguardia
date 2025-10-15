# 📋 Plataforma de Gestión de Reservas

## 📚 Información Académica

- **Asignatura:** Programación de Vanguardia
- **Carrera:** Licenciatura en Tecnologías Informáticas
- **Ciclo Lectivo:** 2025
- **Docente:** Ing. Vázquez Alejandro

## 📖 Descripción del Proyecto

Este proyecto consiste en la migración de una plataforma existente para la gestión de reservas de recursos organizacionales. La migración es necesaria por requerimientos de compliance y debe completarse antes de los cambios de plataforma programados.

### 🔄 Estado Actual del Sistema
- **Tecnología:** Java 8
- **Base de Datos:** SQL Server
- **DAOs:** Desarrollados con JDBC
- **Configuración:** Estática en código fuente

### 🚀 Mejoras Propuestas
- Migración a tecnologías modernas
- Implementación de módulo de predicción de reservas
- Optimización del uso eficiente de recursos
- Configuración dinámica

## 🎯 Objetivos

- [ ] Seleccionar tecnologías adecuadas para el desarrollo del proyecto
- [ ] Desarrollar un MVP (Producto Mínimo Viable)
- [ ] Elegir una base de datos que se adapte mejor a los requisitos
- [ ] Crear mocks de pantallas
- [ ] Definir modelo de pruebas para garantizar la calidad del código
- [ ] Plantear la plataforma de despliegue de la aplicación

## ⚡ Funcionalidades Principales

### 🔐 Autenticación y Autorización
- Registro de usuarios
- Autenticación por roles
- Gestión de permisos

### 📊 Gestión de Datos
- Ingreso y actualización manual de datos
- API para integración de datos
- Recursos reservables

### 🔮 Módulo de Predicción
- Monitor de predicción de reservas
- Análisis de patrones de uso
- Optimización de recursos

## 🗃️ Modelo de Datos

El sistema maneja las siguientes entidades principales:

### 👥 Personas
```sql
CREATE TABLE personas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);
```

### 📦 Artículos
```sql
CREATE TABLE articulos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    disponible BOOLEAN NOT NULL
);
```

### 🏢 Salas
```sql
CREATE TABLE salas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    capacidad INT NOT NULL
);
```

### 📅 Reservas
```sql
CREATE TABLE reservas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_articulo INT,
    id_sala INT,
    id_persona INT NOT NULL,
    fecha_hora_inicio DATETIME NOT NULL,
    fecha_hora_fin DATETIME NOT NULL,
    FOREIGN KEY (id_articulo) REFERENCES articulos(id),
    FOREIGN KEY (id_sala) REFERENCES salas(id),
    FOREIGN KEY (id_persona) REFERENCES personas(id)
);
```

### 📋 Datos de Ejemplo

#### Personas
| ID | Nombre | Email |
|---|---|---|
| 1 | Ana Pérez | ana.perez@organizacion.com |
| 2 | Juan Gómez | juan.gomez@organizacion.com |
| 3 | María López | maria.lopez@organizacion.com |

#### Artículos
| ID | Nombre | Disponible |
|---|---|---|
| 1 | Proyector Epson EB-X05 | ✅ |
| 2 | Laptop HP EliteBook | ❌ |
| 3 | Cámara Sony Alpha a6400 | ✅ |

#### Salas
| ID | Nombre | Capacidad |
|---|---|---|
| 1 | Sala de Reuniones 1A | 8 |
| 2 | Sala de Conferencias B2 | 20 |
| 3 | Aula de Capacitación C3 | 15 |

## 📦 Entregables

### 📅 Fecha Límite: 12 de Noviembre de 2025

### 📋 Componentes Requeridos
- [ ] **Documentación completa** con toda la información relevante
- [ ] **Presentación** en formato PPT o similar
- [ ] **Código fuente** que sustente la Prueba de Concepto (PoC)
- [ ] **Carátula** del proyecto
- [ ] **Presentación de integrantes** del equipo
- [ ] **Gráficos del predictor** de reservas
- [ ] **Diagrama de arquitectura** del sistema
- [ ] **Minutas de reuniones** del equipo
- [ ] **Análisis de mejoras** al problema expuesto

## 🏗️ Arquitectura del Sistema

*[Diagrama de arquitectura será añadido durante el desarrollo]*

## 👥 Equipo de Desarrollo

*[Información del equipo será añadida]*

## 🚀 Instalación y Configuración

*[Instrucciones de instalación serán añadidas durante el desarrollo]*

## 🧪 Pruebas

*[Información sobre pruebas será añadida durante el desarrollo]*

## 📈 Roadmap

- **Fase 1:** Análisis y diseño del sistema
- **Fase 2:** Desarrollo del MVP
- **Fase 3:** Implementación del módulo de predicción
- **Fase 4:** Pruebas y optimización
- **Fase 5:** Despliegue y documentación

## 📄 Licencia

[Información de licencia]

## 🤝 Contribución

[Guías para contribuir al proyecto]

---

*Proyecto desarrollado como parte del trabajo práctico de Programación de Vanguardia - Universidad CAECE*