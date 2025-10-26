-- Crear las tablas y datos iniciales según la consigna
-- Este script se ejecuta automáticamente al inicializar el contenedor

-- Crear tabla personas (usuarios del sistema)
CREATE TABLE IF NOT EXISTS personas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
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
INSERT INTO personas (nombre, email, hashed_password, is_active, is_admin) VALUES
('Admin User', 'admin@organizacion.com', '$2b$12$Io25eHPVYkiIp1MD/EdDHeiuvN8Z2GXF5gSzABi7sE1m7gq6ZcY7i', true, true),
('Ana Pérez', 'ana.perez@organizacion.com', '$2b$12$Io25eHPVYkiIp1MD/EdDHeiuvN8Z2GXF5gSzABi7sE1m7gq6ZcY7i', true, false),
('Juan Gómez', 'juan.gomez@organizacion.com', '$2b$12$Io25eHPVYkiIp1MD/EdDHeiuvN8Z2GXF5gSzABi7sE1m7gq6ZcY7i', true, false),
('María López', 'maria.lopez@organizacion.com', '$2b$12$Io25eHPVYkiIp1MD/EdDHeiuvN8Z2GXF5gSzABi7sE1m7gq6ZcY7i', true, false)
ON CONFLICT (email) DO NOTHING;

INSERT INTO articulos (nombre, descripcion, cantidad, categoria, disponible) VALUES
('Proyector Epson EB-X05', 'Proyector de alta resolución para presentaciones', 3, 'Electrónica', true),
('Laptop HP EliteBook', 'Laptop corporativa para trabajo remoto', 1, 'Informática', false),
('Cámara Sony Alpha a6400', 'Cámara profesional para fotografía y video', 2, 'Fotografía', true)
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

-- Insertar artículos necesarios para reservas de salas (ejemplo: la reserva de sala 2 necesita proyector)
INSERT INTO reserva_articulos (reserva_id, articulo_id, cantidad) VALUES
(2, 1, 1)  -- La reserva 2 (Sala de Conferencias) necesita 1 Proyector
ON CONFLICT DO NOTHING;