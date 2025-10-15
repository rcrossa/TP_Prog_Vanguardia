Trabajo Práctico
Asignatura: Programación de Vanguardia
Carrera: Licenciatura en Tecnologías Informáticas.
Ciclo Lectivo: 2025
Docente: Ing. Vázquez Alejandro.
Plataforma de Gestión de Reservas
Descripción
Se desea migrar una plataforma existente en el cual se quiere utilizar una
herramienta para poder llevar las reservas de recursos en la organización. Por
cuestiones de compliance se debe hacer la migración para poder seguir operando
antes de los cambios de plataformas.
Se desea además agregar un módulo de predicción de reservas para hacer uso
eficiente de los recursos.
El sistema a migrar está desarrollado en Java 8, con una base de datos Sql Server,
donde los Dao 's estaban desarrollados con jdbc. Y varias configuraciones estaban
estáticas en el código fuente.
Objetivo
● Seleccionar tecnologías adecuadas para el desarrollo del proyecto.
● Realizar una MVP(una propuesta mínima viable posible).
● Elegir una base de datos que se adapte mejor a los requisitos del proyecto.
● Crear mocks de pantallas.
● Definir modelo de pruebas para garantizar la calidad del código.
● Plantear la plataforma donde se realizará el despliegue de la aplicación.
Funcionalidades Principales
● Registro y autenticación de usuarios por roles.
● Ingreso y actualización de datos manual y vía api que se pueden reservar.
● Monitor de predicción de reservas.
Modelo de datos existentes
Se dispone del siguiente modelo de datos, el cual puede ser ajustado.
CREATE TABLE personas (
id INT PRIMARY KEY AUTO_INCREMENT,
nombre VARCHAR(255) NOT NULL,
email VARCHAR(255) UNIQUE NOT NULL
);
INSERT INTO personas (id, nombre, email) VALUES
(1, 'Ana Pérez', 'ana.perez@organizacion.com'),
(2, 'Juan Gómez', 'juan.gomez@organizacion.com'),
(3, 'María López', 'maria.lopez@organizacion.com');
CREATE TABLE articulos (
id INT PRIMARY KEY AUTO_INCREMENT,
nombre VARCHAR(255) NOT NULL,
disponible BOOLEAN NOT NULL
);
INSERT INTO articulos (id, nombre, disponible) VALUES
(1, 'Proyector Epson EB-X05', 1),
(2, 'Laptop HP EliteBook', 0),
(3, 'Cámara Sony Alpha a6400', 1);
CREATE TABLE salas (
id INT PRIMARY KEY AUTO_INCREMENT,
nombre VARCHAR(255) NOT NULL,
capacidad INT NOT NULL
);
INSERT INTO salas (id, nombre, capacidad) VALUES
(1, 'Sala de Reuniones 1A', 8),
(2, 'Sala de Conferencias B2', 20),
(3, 'Aula de Capacitación C3', 15);
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
INSERT INTO reservas (id_articulo, id_sala, id_persona, fecha_hora_inicio,
fecha_hora_fin) VALUES
(1, NULL, 1, '2025-09-11 10:00:00', '2025-09-11 11:00:00'),
(NULL, 2, 2, '2025-09-12 14:00:00', '2025-09-12 16:00:00'),
(2, NULL, 3, '2025-09-13 09:00:00', '2025-09-13 10:00:00');
Entregable
● Documento con toda la información relevante hasta la fecha del 12-11
● Presentación en formato ppt o similar.
● Código que sustente la PoC.
Nota: Formato de la entrega, carátula, presentación de los integrantes, código,
gráficos del predictor. Diagrama de arquitectura. Todos los puntos que sean
relevantes, como así también minutas de reuniones.
Ejemplo del código que se desea migrar
Nota: Pensar en mejoras al problema expuesto.