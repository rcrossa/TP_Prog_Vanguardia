-- Crear las tablas y datos iniciales según la consigna
-- Este script se ejecuta automáticamente al inicializar el contenedor

-- Crear tabla personas
CREATE TABLE IF NOT EXISTS personas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Crear tabla articulos
CREATE TABLE IF NOT EXISTS articulos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    disponible BOOLEAN NOT NULL
);

-- Crear tabla salas
CREATE TABLE IF NOT EXISTS salas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    capacidad INTEGER NOT NULL
);

-- Crear tabla reservas
CREATE TABLE IF NOT EXISTS reservas (
    id SERIAL PRIMARY KEY,
    id_articulo INTEGER REFERENCES articulos(id),
    id_sala INTEGER REFERENCES salas(id),
    id_persona INTEGER NOT NULL REFERENCES personas(id),
    fecha_hora_inicio TIMESTAMP NOT NULL,
    fecha_hora_fin TIMESTAMP NOT NULL
);

-- Insertar datos de ejemplo según la consigna
INSERT INTO personas (nombre, email) VALUES
('Ana Pérez', 'ana.perez@organizacion.com'),
('Juan Gómez', 'juan.gomez@organizacion.com'),
('María López', 'maria.lopez@organizacion.com')
ON CONFLICT (email) DO NOTHING;

INSERT INTO articulos (nombre, disponible) VALUES
('Proyector Epson EB-X05', true),
('Laptop HP EliteBook', false),
('Cámara Sony Alpha a6400', true)
ON CONFLICT DO NOTHING;

INSERT INTO salas (nombre, capacidad) VALUES
('Sala de Reuniones 1A', 8),
('Sala de Conferencias B2', 20),
('Aula de Capacitación C3', 15)
ON CONFLICT DO NOTHING;

INSERT INTO reservas (id_articulo, id_sala, id_persona, fecha_hora_inicio, fecha_hora_fin) VALUES
(1, NULL, 1, '2025-09-11 10:00:00', '2025-09-11 11:00:00'),
(NULL, 2, 2, '2025-09-12 14:00:00', '2025-09-12 16:00:00'),
(2, NULL, 3, '2025-09-13 09:00:00', '2025-09-13 10:00:00')
ON CONFLICT DO NOTHING;