"""
Script para inicializar la base de datos con los datos de ejemplo de la consigna
"""


from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
from app.auth.jwt_handler import get_password_hash
from app.core.database import Base, SessionLocal
from app.models import Articulo, Persona, Reserva, Sala
from app.core.database import engine


def init_database():
    """Crear las tablas y cargar datos de ejemplo"""

    # Crear todas las tablas

    Base.metadata.create_all(bind=engine)

    # Crear sesión
    db = SessionLocal()

    try:
        # Verificar si ya hay datos
        if db.query(Persona).count() > 0:
            print("La base de datos ya contiene datos.")
            return

        # Insertar personas (según la consigna) con contraseñas de prueba y nuevos campos
        personas = [
            Persona(
                nombre="Ana Pérez",
                apellido="Pérez",
                email="ana.perez@organizacion.com",
                hashed_password=get_password_hash("admin123"),
                is_active=True,
                is_admin=True,
                created_at=datetime.now(timezone.utc),
                last_login=None,
            ),
            Persona(
                nombre="Juan Gómez",
                apellido="Gómez",
                email="juan.gomez@organizacion.com",
                hashed_password=get_password_hash("user123"),
                is_active=True,
                is_admin=False,
                created_at=datetime.now(timezone.utc),
                last_login=None,
            ),
            Persona(
                nombre="María López",
                apellido="López",
                email="maria.lopez@organizacion.com",
                hashed_password=get_password_hash("user123"),
                is_active=True,
                is_admin=False,
                created_at=datetime.now(timezone.utc),
                last_login=None,
            ),
        ]

        for persona in personas:
            db.add(persona)

        # Insertar artículos (según la consigna) con nuevos campos
        articulos = [
            Articulo(
                nombre="Proyector Epson EB-X05",
                descripcion="Proyector XGA 3.300 lúmenes",
                cantidad=1,
                categoria="Proyector",
                disponible=True,
            ),
            Articulo(
                nombre="Laptop HP EliteBook",
                descripcion="Notebook 14'' Intel i5",
                cantidad=1,
                categoria="Laptop",
                disponible=False,
            ),
            Articulo(
                nombre="Cámara Sony Alpha a6400",
                descripcion="Cámara mirrorless 24MP",
                cantidad=1,
                categoria="Cámara",
                disponible=True,
            ),
        ]

        for articulo in articulos:
            db.add(articulo)

        # Insertar salas (según la consigna) con nuevos campos
        salas = [
            Sala(
                nombre="Sala de Reuniones 1A",
                capacidad=8,
                disponible=True,
                ubicacion="Edificio A, piso 1",
                descripcion="Sala pequeña para reuniones",
            ),
            Sala(
                nombre="Sala de Conferencias B2",
                capacidad=20,
                disponible=True,
                ubicacion="Edificio B, piso 2",
                descripcion="Sala grande para conferencias",
            ),
            Sala(
                nombre="Aula de Capacitación C3",
                capacidad=15,
                disponible=True,
                ubicacion="Edificio C, piso 3",
                descripcion="Aula equipada para capacitaciones",
            ),
        ]

        for sala in salas:
            db.add(sala)

        # Insertar reservas (según la consigna, sin asignar id manualmente)
        reservas = [
            Reserva(
                id_articulo=1,
                id_sala=None,
                id_persona=1,
                fecha_hora_inicio=datetime(2025, 9, 11, 10, 0, 0),
                fecha_hora_fin=datetime(2025, 9, 11, 11, 0, 0),
            ),
            Reserva(
                id_articulo=None,
                id_sala=2,
                id_persona=2,
                fecha_hora_inicio=datetime(2025, 9, 12, 14, 0, 0),
                fecha_hora_fin=datetime(2025, 9, 12, 16, 0, 0),
            ),
            Reserva(
                id_articulo=2,
                id_sala=None,
                id_persona=3,
                fecha_hora_inicio=datetime(2025, 9, 13, 9, 0, 0),
                fecha_hora_fin=datetime(2025, 9, 13, 10, 0, 0),
            ),
        ]

        for reserva in reservas:
            db.add(reserva)

        # Guardar cambios
        db.commit()
        print("Base de datos inicializada exitosamente con los datos de ejemplo.")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al inicializar la base de datos: {e}")
    finally:
        db.close()
        db.close()


if __name__ == "__main__":
    init_database()
