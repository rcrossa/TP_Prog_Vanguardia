"""
Script para inicializar la base de datos con los datos de ejemplo de la consigna
"""
from datetime import datetime
from app.core.database import Base, SessionLocal
from app.models import Persona, Articulo, Sala, Reserva


def init_database():
    """Crear las tablas y cargar datos de ejemplo"""
    
    # Crear todas las tablas
    from app.core.database import engine
    Base.metadata.create_all(bind=engine)
    
    # Crear sesión
    db = SessionLocal()
    
    try:
        # Verificar si ya hay datos
        if db.query(Persona).count() > 0:
            print("La base de datos ya contiene datos.")
            return
        
        # Insertar personas (según la consigna)
        personas = [
            Persona(id=1, nombre="Ana Pérez", email="ana.perez@organizacion.com"),
            Persona(id=2, nombre="Juan Gómez", email="juan.gomez@organizacion.com"),
            Persona(id=3, nombre="María López", email="maria.lopez@organizacion.com")
        ]
        
        for persona in personas:
            db.add(persona)
        
        # Insertar artículos (según la consigna)
        articulos = [
            Articulo(id=1, nombre="Proyector Epson EB-X05", disponible=True),
            Articulo(id=2, nombre="Laptop HP EliteBook", disponible=False),
            Articulo(id=3, nombre="Cámara Sony Alpha a6400", disponible=True)
        ]
        
        for articulo in articulos:
            db.add(articulo)
        
        # Insertar salas (según la consigna)
        salas = [
            Sala(id=1, nombre="Sala de Reuniones 1A", capacidad=8),
            Sala(id=2, nombre="Sala de Conferencias B2", capacidad=20),
            Sala(id=3, nombre="Aula de Capacitación C3", capacidad=15)
        ]
        
        for sala in salas:
            db.add(sala)
        
        # Insertar reservas (según la consigna)
        reservas = [
            Reserva(
                id_articulo=1,
                id_sala=None,
                id_persona=1,
                fecha_hora_inicio=datetime(2025, 9, 11, 10, 0, 0),
                fecha_hora_fin=datetime(2025, 9, 11, 11, 0, 0)
            ),
            Reserva(
                id_articulo=None,
                id_sala=2,
                id_persona=2,
                fecha_hora_inicio=datetime(2025, 9, 12, 14, 0, 0),
                fecha_hora_fin=datetime(2025, 9, 12, 16, 0, 0)
            ),
            Reserva(
                id_articulo=2,
                id_sala=None,
                id_persona=3,
                fecha_hora_inicio=datetime(2025, 9, 13, 9, 0, 0),
                fecha_hora_fin=datetime(2025, 9, 13, 10, 0, 0)
            )
        ]
        
        for reserva in reservas:
            db.add(reserva)
        
        # Guardar cambios
        db.commit()
        print("Base de datos inicializada exitosamente con los datos de ejemplo.")
        
    except Exception as e:
        db.rollback()
        print(f"Error al inicializar la base de datos: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    init_database()