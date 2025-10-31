-- Crear las tablas y datos iniciales según la consigna
-- Este script se ejecuta automáticamente al inicializar el contenedor

-- Crear tabla personas (usuarios del sistema)
CREATE TABLE IF NOT EXISTS personas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT true,
    is_admin BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

-- Crear tabla articulos
CREATE TABLE IF NOT EXISTS articulos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255),
    cantidad INTEGER NOT NULL DEFAULT 1,
    categoria VARCHAR(255),
    disponible BOOLEAN NOT NULL DEFAULT true
);

-- Crear tabla salas
CREATE TABLE IF NOT EXISTS salas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    capacidad INTEGER NOT NULL,
    disponible BOOLEAN NOT NULL DEFAULT true,
    ubicacion VARCHAR(255) DEFAULT '',
    descripcion VARCHAR(255) DEFAULT ''
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

-- Crear tabla de relación muchos-a-muchos entre reservas de salas y artículos necesarios
CREATE TABLE IF NOT EXISTS reserva_articulos (
    reserva_id INTEGER NOT NULL REFERENCES reservas(id) ON DELETE CASCADE,
    articulo_id INTEGER NOT NULL REFERENCES articulos(id) ON DELETE CASCADE,
    cantidad INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (reserva_id, articulo_id)
);

-- ============================================================================
-- DATOS DE EJEMPLO - SOLO PARA DESARROLLO Y TESTING
-- ============================================================================
-- ⚠️ IMPORTANTE: NO USAR ESTOS DATOS EN PRODUCCIÓN
-- 
-- Las contraseñas están hasheadas con bcrypt (nunca en texto plano)
-- Para fines de demostración, todos los usuarios usan: "admin123"
-- Hash bcrypt generado: $2b$12$Io25eHPVYkiIp1MD/EdDHeiuvN8Z2GXF5gSzABi7sE1m7gq6ZcY7i
-- 
-- En producción:
-- 1. Eliminar estos INSERT statements
-- 2. Crear usuarios solo vía API: POST /api/v1/auth/register
-- 3. Forzar cambio de contraseña en primer login
-- 4. Usar contraseñas únicas y fuertes
-- ============================================================================

-- Insertar personas
INSERT INTO personas (nombre, apellido, email, hashed_password, is_active, is_admin) VALUES
('Admin', 'User', 'admin@organizacion.com', '$2b$12$Io25eHPVYkiIp1MD/EdDHeiuvN8Z2GXF5gSzABi7sE1m7gq6ZcY7i', true, true),
('Ana', 'Pérez', 'ana.perez@organizacion.com', '$2b$12$Io25eHPVYkiIp1MD/EdDHeiuvN8Z2GXF5gSzABi7sE1m7gq6ZcY7i', true, false),
('Juan', 'Gómez', 'juan.gomez@organizacion.com', '$2b$12$Io25eHPVYkiIp1MD/EdDHeiuvN8Z2GXF5gSzABi7sE1m7gq6ZcY7i', true, false),
('María', 'López', 'maria.lopez@organizacion.com', '$2b$12$Io25eHPVYkiIp1MD/EdDHeiuvN8Z2GXF5gSzABi7sE1m7gq6ZcY7i', true, false),
('Carlos', 'Rodríguez', 'carlos.rodriguez@organizacion.com', '$2b$12$Io25eHPVYkiIp1MD/EdDHeiuvN8Z2GXF5gSzABi7sE1m7gq6ZcY7i', true, false),
('Sofia', 'Fernández', 'sofia.fernandez@organizacion.com', '$2b$12$Io25eHPVYkiIp1MD/EdDHeiuvN8Z2GXF5gSzABi7sE1m7gq6ZcY7i', true, false),
('Diego', 'Sánchez', 'diego.sanchez@organizacion.com', '$2b$12$Io25eHPVYkiIp1MD/EdDHeiuvN8Z2GXF5gSzABi7sE1m7gq6ZcY7i', true, false)
ON CONFLICT (email) DO NOTHING;

-- Insertar artículos variados
INSERT INTO articulos (nombre, descripcion, cantidad, categoria, disponible) VALUES
('Proyector Epson EB-X05', 'Proyector de alta resolución para presentaciones', 5, 'Electrónica', true),
('Laptop HP EliteBook', 'Laptop corporativa para trabajo remoto', 3, 'Informática', true),
('Cámara Sony Alpha a6400', 'Cámara profesional para fotografía y video', 2, 'Fotografía', true),
('Pizarra Blanca Portátil', 'Pizarra con ruedas y marcadores', 8, 'Oficina', true),
('Micrófono Inalámbrico', 'Micrófono de solapa profesional', 4, 'Audio', true),
('Cable HDMI 2m', 'Cable HDMI de alta velocidad', 15, 'Conectividad', true),
('Adaptador VGA a HDMI', 'Convertidor de señal de video', 10, 'Conectividad', true),
('Extensión Eléctrica 5m', 'Zapatilla de 6 tomas con cable largo', 12, 'Electricidad', true),
('Marcadores de Colores', 'Set de 12 marcadores para pizarra', 25, 'Oficina', true),
('Parlantes Bluetooth', 'Sistema de audio portátil', 6, 'Audio', true),
('Tablet Samsung Galaxy', 'Tablet 10 pulgadas para presentaciones', 4, 'Informática', true),
('Webcam Logitech HD', 'Cámara web Full HD', 8, 'Informática', true),
('Router WiFi', 'Router portátil para eventos', 3, 'Conectividad', true),
('Mouse Inalámbrico', 'Mouse ergonómico', 20, 'Informática', true),
('Teclado Inalámbrico', 'Teclado compacto', 15, 'Informática', true)
ON CONFLICT DO NOTHING;

-- Insertar salas
INSERT INTO salas (nombre, capacidad, ubicacion, descripcion) VALUES
('Sala de Reuniones 1A', 8, 'Edificio A, Piso 1', 'Sala pequeña para equipos'),
('Sala de Conferencias B2', 20, 'Edificio B, Piso 2', 'Sala grande con proyector'),
('Aula de Capacitación C3', 15, 'Edificio C, Piso 3', 'Aula equipada para training'),
('Sala Ejecutiva', 10, 'Edificio A, Piso 3', 'Sala premium para directivos'),
('Sala Innovación', 12, 'Edificio B, Piso 1', 'Espacio colaborativo'),
('Sala de Reuniones 2A', 6, 'Edificio A, Piso 2', 'Sala pequeña')
ON CONFLICT DO NOTHING;

-- Insertar reservas históricas (julio a octubre 2025)
-- Mezcla de reservas de salas, artículos individuales y combinaciones

-- Reservas de JULIO 2025
INSERT INTO reservas (id_articulo, id_sala, id_persona, fecha_hora_inicio, fecha_hora_fin) VALUES
-- Semana 1 de julio
(1, NULL, 2, '2025-07-01 09:15:00', '2025-07-01 11:45:00'),
(NULL, 1, 3, '2025-07-01 14:20:00', '2025-07-01 16:30:00'),
(5, NULL, 4, '2025-07-02 10:00:00', '2025-07-02 12:00:00'),
(NULL, 2, 5, '2025-07-02 13:45:00', '2025-07-02 15:15:00'),
(11, NULL, 6, '2025-07-03 09:30:00', '2025-07-03 11:00:00'),
(NULL, 3, 2, '2025-07-03 14:00:00', '2025-07-03 16:00:00'),
(3, NULL, 4, '2025-07-04 10:15:00', '2025-07-04 12:45:00'),
(NULL, 4, 5, '2025-07-04 15:15:00', '2025-07-04 17:45:00'),

-- Semana 2 de julio
(2, NULL, 3, '2025-07-07 09:00:00', '2025-07-07 10:30:00'),
(NULL, 5, 6, '2025-07-07 14:30:00', '2025-07-07 17:15:00'),
(7, NULL, 2, '2025-07-08 11:15:00', '2025-07-08 13:45:00'),
(NULL, 1, 4, '2025-07-08 09:45:00', '2025-07-08 12:15:00'),
(NULL, 2, 5, '2025-07-09 14:00:00', '2025-07-09 16:30:00'),
(12, NULL, 6, '2025-07-09 10:20:00', '2025-07-09 11:50:00'),
(NULL, 3, 2, '2025-07-10 13:30:00', '2025-07-10 15:00:00'),
(1, NULL, 3, '2025-07-10 09:15:00', '2025-07-10 11:45:00'),
(NULL, 4, 4, '2025-07-11 14:45:00', '2025-07-11 17:15:00'),

-- Semana 3 de julio
(5, NULL, 5, '2025-07-14 09:30:00', '2025-07-14 12:00:00'),
(NULL, 5, 6, '2025-07-14 13:15:00', '2025-07-14 15:45:00'),
(NULL, 1, 2, '2025-07-15 10:00:00', '2025-07-15 12:30:00'),
(3, NULL, 3, '2025-07-15 14:20:00', '2025-07-15 16:50:00'),
(NULL, 2, 4, '2025-07-16 09:45:00', '2025-07-16 11:15:00'),
(11, NULL, 5, '2025-07-16 13:00:00', '2025-07-16 15:30:00'),
(NULL, 3, 6, '2025-07-17 10:15:00', '2025-07-17 12:45:00'),
(2, NULL, 2, '2025-07-17 14:30:00', '2025-07-17 17:00:00'),
(NULL, 4, 3, '2025-07-18 09:00:00', '2025-07-18 11:00:00'),

-- Semana 4 de julio
(7, NULL, 4, '2025-07-21 13:45:00', '2025-07-21 16:15:00'),
(NULL, 5, 5, '2025-07-21 10:30:00', '2025-07-21 12:00:00'),
(NULL, 1, 6, '2025-07-22 14:15:00', '2025-07-22 16:45:00'),
(1, NULL, 2, '2025-07-22 09:15:00', '2025-07-22 11:45:00'),
(NULL, 2, 3, '2025-07-23 13:30:00', '2025-07-23 15:00:00'),
(12, NULL, 4, '2025-07-23 10:00:00', '2025-07-23 12:30:00'),
(NULL, 3, 5, '2025-07-24 14:45:00', '2025-07-24 17:15:00'),
(5, NULL, 6, '2025-07-24 09:30:00', '2025-07-24 11:00:00'),
(NULL, 4, 2, '2025-07-25 13:15:00', '2025-07-25 15:45:00'),

-- Última semana julio
(3, NULL, 3, '2025-07-28 10:15:00', '2025-07-28 12:45:00'),
(NULL, 5, 4, '2025-07-28 14:00:00', '2025-07-28 16:30:00'),
(NULL, 1, 5, '2025-07-29 09:45:00', '2025-07-29 11:15:00'),
(11, NULL, 6, '2025-07-29 13:30:00', '2025-07-29 16:00:00'),
(NULL, 2, 2, '2025-07-30 10:20:00', '2025-07-30 12:50:00'),
(2, NULL, 3, '2025-07-30 14:15:00', '2025-07-30 16:45:00'),
(NULL, 3, 4, '2025-07-31 09:00:00', '2025-07-31 11:30:00'),

-- Reservas de AGOSTO 2025
-- Semana 1 de agosto
(7, NULL, 5, '2025-08-01 13:45:00', '2025-08-01 16:15:00'),
(NULL, 4, 6, '2025-08-01 10:15:00', '2025-08-01 12:45:00'),
(NULL, 5, 2, '2025-08-04 14:30:00', '2025-08-04 17:00:00'),
(1, NULL, 3, '2025-08-04 09:30:00', '2025-08-04 11:00:00'),
(NULL, 1, 4, '2025-08-05 13:15:00', '2025-08-05 15:45:00'),
(12, NULL, 5, '2025-08-05 10:00:00', '2025-08-05 12:30:00'),
(NULL, 2, 6, '2025-08-06 14:45:00', '2025-08-06 17:15:00'),
(5, NULL, 2, '2025-08-06 09:15:00', '2025-08-06 11:45:00'),
(NULL, 3, 3, '2025-08-07 13:30:00', '2025-08-07 16:00:00'),
(3, NULL, 4, '2025-08-07 10:30:00', '2025-08-07 12:00:00'),
(NULL, 4, 5, '2025-08-08 14:15:00', '2025-08-08 16:45:00'),

-- Semana 2 de agosto
(11, NULL, 6, '2025-08-11 09:45:00', '2025-08-11 11:15:00'),
(NULL, 5, 2, '2025-08-11 13:00:00', '2025-08-11 15:30:00'),
(2, NULL, 3, '2025-08-12 10:15:00', '2025-08-12 12:45:00'),
(NULL, 1, 4, '2025-08-12 14:30:00', '2025-08-12 17:00:00'),
(7, NULL, 5, '2025-08-13 09:30:00', '2025-08-13 11:00:00'),
(NULL, 2, 6, '2025-08-13 13:45:00', '2025-08-13 16:15:00'),
(1, NULL, 2, '2025-08-14 10:00:00', '2025-08-14 12:30:00'),
(NULL, 3, 3, '2025-08-14 14:15:00', '2025-08-14 16:45:00'),
(12, NULL, 4, '2025-08-15 09:15:00', '2025-08-15 11:45:00'),
(NULL, 4, 5, '2025-08-15 13:30:00', '2025-08-15 16:00:00'),

-- Semana 3 de agosto
(5, NULL, 6, '2025-08-18 10:30:00', '2025-08-18 12:00:00'),
(NULL, 5, 2, '2025-08-18 14:45:00', '2025-08-18 17:15:00'),
(3, NULL, 3, '2025-08-19 09:45:00', '2025-08-19 11:15:00'),
(NULL, 1, 4, '2025-08-19 13:15:00', '2025-08-19 15:45:00'),
(11, NULL, 5, '2025-08-20 10:15:00', '2025-08-20 12:45:00'),
(NULL, 2, 6, '2025-08-20 14:00:00', '2025-08-20 16:30:00'),
(2, NULL, 2, '2025-08-21 09:30:00', '2025-08-21 11:00:00'),
(NULL, 3, 3, '2025-08-21 13:45:00', '2025-08-21 16:15:00'),
(7, NULL, 4, '2025-08-22 10:00:00', '2025-08-22 12:30:00'),
(NULL, 4, 5, '2025-08-22 14:30:00', '2025-08-22 17:00:00'),

-- Semana 4 de agosto
(1, NULL, 6, '2025-08-25 09:15:00', '2025-08-25 11:45:00'),
(NULL, 5, 2, '2025-08-25 13:30:00', '2025-08-25 16:00:00'),
(12, NULL, 3, '2025-08-26 10:30:00', '2025-08-26 12:00:00'),
(NULL, 1, 4, '2025-08-26 14:15:00', '2025-08-26 16:45:00'),
(5, NULL, 5, '2025-08-27 09:45:00', '2025-08-27 11:15:00'),
(NULL, 2, 6, '2025-08-27 13:00:00', '2025-08-27 15:30:00'),
(3, NULL, 2, '2025-08-28 10:15:00', '2025-08-28 12:45:00'),
(NULL, 3, 3, '2025-08-28 14:45:00', '2025-08-28 17:15:00'),
(11, NULL, 4, '2025-08-29 09:30:00', '2025-08-29 11:00:00'),
(NULL, 4, 5, '2025-08-29 13:15:00', '2025-08-29 15:45:00'),

-- Reservas de SEPTIEMBRE 2025
-- Semana 1 de septiembre
(2, NULL, 6, '2025-09-01 10:00:00', '2025-09-01 12:30:00'),
(NULL, 5, 2, '2025-09-01 14:30:00', '2025-09-01 17:00:00'),
(7, NULL, 3, '2025-09-02 09:15:00', '2025-09-02 11:45:00'),
(NULL, 1, 4, '2025-09-02 13:45:00', '2025-09-02 16:15:00'),
(1, NULL, 5, '2025-09-03 10:30:00', '2025-09-03 12:00:00'),
(NULL, 2, 6, '2025-09-03 14:15:00', '2025-09-03 16:45:00'),
(12, NULL, 2, '2025-09-04 09:45:00', '2025-09-04 11:15:00'),
(NULL, 3, 3, '2025-09-04 13:30:00', '2025-09-04 16:00:00'),
(5, NULL, 4, '2025-09-05 10:15:00', '2025-09-05 12:45:00'),
(NULL, 4, 5, '2025-09-05 14:00:00', '2025-09-05 16:30:00'),

-- Semana 2 de septiembre
(3, NULL, 6, '2025-09-08 09:30:00', '2025-09-08 11:00:00'),
(NULL, 5, 2, '2025-09-08 13:15:00', '2025-09-08 15:45:00'),
(11, NULL, 3, '2025-09-09 10:00:00', '2025-09-09 12:30:00'),
(NULL, 1, 4, '2025-09-09 14:45:00', '2025-09-09 17:15:00'),
(2, NULL, 5, '2025-09-10 09:15:00', '2025-09-10 11:45:00'),
(NULL, 2, 6, '2025-09-10 13:30:00', '2025-09-10 16:00:00'),
(7, NULL, 2, '2025-09-11 10:30:00', '2025-09-11 12:00:00'),
(NULL, 3, 3, '2025-09-11 14:15:00', '2025-09-11 16:45:00'),
(1, NULL, 4, '2025-09-12 09:45:00', '2025-09-12 11:15:00'),
(NULL, 4, 5, '2025-09-12 13:00:00', '2025-09-12 15:30:00'),

-- Semana 3 de septiembre
(12, NULL, 6, '2025-09-15 10:15:00', '2025-09-15 12:45:00'),
(NULL, 5, 2, '2025-09-15 14:30:00', '2025-09-15 17:00:00'),
(5, NULL, 3, '2025-09-16 09:30:00', '2025-09-16 11:00:00'),
(NULL, 1, 4, '2025-09-16 13:45:00', '2025-09-16 16:15:00'),
(3, NULL, 5, '2025-09-17 10:00:00', '2025-09-17 12:30:00'),
(NULL, 2, 6, '2025-09-17 14:15:00', '2025-09-17 16:45:00'),
(11, NULL, 2, '2025-09-18 09:15:00', '2025-09-18 11:45:00'),
(NULL, 3, 3, '2025-09-18 13:30:00', '2025-09-18 16:00:00'),
(2, NULL, 4, '2025-09-19 10:30:00', '2025-09-19 12:00:00'),
(NULL, 4, 5, '2025-09-19 14:45:00', '2025-09-19 17:15:00'),

-- Semana 4 de septiembre
(7, NULL, 6, '2025-09-22 09:45:00', '2025-09-22 11:15:00'),
(NULL, 5, 2, '2025-09-22 13:15:00', '2025-09-22 15:45:00'),
(1, NULL, 3, '2025-09-23 10:15:00', '2025-09-23 12:45:00'),
(NULL, 1, 4, '2025-09-23 14:00:00', '2025-09-23 16:30:00'),
(12, NULL, 5, '2025-09-24 09:30:00', '2025-09-24 11:00:00'),
(NULL, 2, 6, '2025-09-24 13:45:00', '2025-09-24 16:15:00'),
(5, NULL, 2, '2025-09-25 10:00:00', '2025-09-25 12:30:00'),
(NULL, 3, 3, '2025-09-25 14:30:00', '2025-09-25 17:00:00'),
(3, NULL, 4, '2025-09-26 09:15:00', '2025-09-26 11:45:00'),
(NULL, 4, 5, '2025-09-26 13:30:00', '2025-09-26 16:00:00'),

-- Última semana septiembre
(11, NULL, 6, '2025-09-29 10:30:00', '2025-09-29 12:00:00'),
(NULL, 5, 2, '2025-09-29 14:15:00', '2025-09-29 16:45:00'),
(2, NULL, 3, '2025-09-30 09:45:00', '2025-09-30 11:15:00'),
(NULL, 1, 4, '2025-09-30 13:00:00', '2025-09-30 15:30:00'),

-- Reservas de OCTUBRE 2025
-- Semana 1 de octubre
(7, NULL, 5, '2025-10-01 10:15:00', '2025-10-01 12:45:00'),
(NULL, 2, 6, '2025-10-01 14:45:00', '2025-10-01 17:15:00'),
(1, NULL, 2, '2025-10-02 09:30:00', '2025-10-02 11:00:00'),
(NULL, 3, 3, '2025-10-02 13:15:00', '2025-10-02 15:45:00'),
(12, NULL, 4, '2025-10-03 10:00:00', '2025-10-03 12:30:00'),
(NULL, 4, 5, '2025-10-03 14:30:00', '2025-10-03 17:00:00'),

-- Semana 2 de octubre
(5, NULL, 6, '2025-10-06 09:15:00', '2025-10-06 11:45:00'),
(NULL, 5, 2, '2025-10-06 13:30:00', '2025-10-06 16:00:00'),
(3, NULL, 3, '2025-10-07 10:30:00', '2025-10-07 12:00:00'),
(NULL, 1, 4, '2025-10-07 14:15:00', '2025-10-07 16:45:00'),
(11, NULL, 5, '2025-10-08 09:45:00', '2025-10-08 11:15:00'),
(NULL, 2, 6, '2025-10-08 13:00:00', '2025-10-08 15:30:00'),
(2, NULL, 2, '2025-10-09 10:15:00', '2025-10-09 12:45:00'),
(NULL, 3, 3, '2025-10-09 14:45:00', '2025-10-09 17:15:00'),
(7, NULL, 4, '2025-10-10 09:30:00', '2025-10-10 11:00:00'),
(NULL, 4, 5, '2025-10-10 13:15:00', '2025-10-10 15:45:00'),

-- Semana 3 de octubre
(1, NULL, 6, '2025-10-13 10:00:00', '2025-10-13 12:30:00'),
(NULL, 5, 2, '2025-10-13 14:30:00', '2025-10-13 17:00:00'),
(12, NULL, 3, '2025-10-14 09:15:00', '2025-10-14 11:45:00'),
(NULL, 1, 4, '2025-10-14 13:45:00', '2025-10-14 16:15:00'),
(5, NULL, 5, '2025-10-15 10:30:00', '2025-10-15 12:00:00'),
(NULL, 2, 6, '2025-10-15 14:15:00', '2025-10-15 16:45:00'),
(3, NULL, 2, '2025-10-16 09:45:00', '2025-10-16 11:15:00'),
(NULL, 3, 3, '2025-10-16 13:30:00', '2025-10-16 16:00:00'),
(11, NULL, 4, '2025-10-17 10:15:00', '2025-10-17 12:45:00'),
(NULL, 4, 5, '2025-10-17 14:00:00', '2025-10-17 16:30:00'),

-- Semana 4 de octubre
(2, NULL, 6, '2025-10-20 09:30:00', '2025-10-20 11:00:00'),
(NULL, 5, 2, '2025-10-20 13:15:00', '2025-10-20 15:45:00'),
(7, NULL, 3, '2025-10-21 10:00:00', '2025-10-21 12:30:00'),
(NULL, 1, 4, '2025-10-21 14:45:00', '2025-10-21 17:15:00'),
(1, NULL, 5, '2025-10-22 09:15:00', '2025-10-22 11:45:00'),
(NULL, 2, 6, '2025-10-22 13:30:00', '2025-10-22 16:00:00'),
(12, NULL, 2, '2025-10-23 10:30:00', '2025-10-23 12:00:00'),
(NULL, 3, 3, '2025-10-23 14:15:00', '2025-10-23 16:45:00'),
(5, NULL, 4, '2025-10-24 09:45:00', '2025-10-24 11:15:00'),
(NULL, 4, 5, '2025-10-24 13:00:00', '2025-10-24 15:30:00'),

-- Última semana octubre (hasta el 30)
(3, NULL, 6, '2025-10-27 10:15:00', '2025-10-27 12:45:00'),
(NULL, 5, 2, '2025-10-27 14:30:00', '2025-10-27 17:00:00'),
(11, NULL, 3, '2025-10-28 09:30:00', '2025-10-28 11:00:00'),
(NULL, 1, 4, '2025-10-28 13:45:00', '2025-10-28 16:15:00'),
(2, NULL, 5, '2025-10-29 10:00:00', '2025-10-29 12:30:00'),
(NULL, 2, 6, '2025-10-29 14:15:00', '2025-10-29 16:45:00'),
(7, NULL, 2, '2025-10-30 09:15:00', '2025-10-30 11:45:00'),
(NULL, 3, 3, '2025-10-30 13:30:00', '2025-10-30 16:00:00')
ON CONFLICT DO NOTHING;

-- Insertar artículos necesarios para reservas de salas
-- (Relacionar algunas reservas de sala con artículos adicionales)
INSERT INTO reserva_articulos (reserva_id, articulo_id, cantidad) VALUES
-- Algunas salas de julio con equipamiento
(2, 1, 1), (2, 5, 2),
(6, 4, 1), (6, 9, 1),
(10, 2, 1), (10, 10, 1),
(13, 1, 1), (13, 6, 2),
(17, 12, 1), (17, 5, 1),
-- Algunas salas de agosto con equipamiento
(22, 1, 1), (22, 7, 1),
(26, 11, 2), (26, 10, 1),
(30, 4, 1), (30, 9, 2),
(35, 2, 1), (35, 6, 1),
(39, 1, 1), (39, 8, 1),
-- Algunas salas de septiembre con equipamiento
(43, 12, 1), (43, 5, 1),
(47, 1, 1), (47, 6, 2),
(51, 4, 1), (51, 9, 1),
(56, 2, 1), (56, 10, 1),
(60, 11, 1), (60, 8, 1),
-- Algunas salas de octubre con equipamiento
(64, 1, 1), (64, 5, 2),
(68, 12, 1), (68, 6, 1),
(73, 4, 1), (73, 9, 2),
(77, 2, 1), (77, 10, 1),
(81, 1, 1), (81, 7, 1)
ON CONFLICT DO NOTHING;