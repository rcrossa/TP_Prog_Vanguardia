"""
Script para inicializar la base de datos con datos de ejemplo
"""

from datetime import datetime, timedelta, timezone
import random
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from app.core.database import Base, SessionLocal, engine
from app.models.persona import Persona
from app.models.sala import Sala
from app.models.articulo import Articulo
from app.models.reserva import Reserva

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def init_database():
    """Crear las tablas y cargar datos de ejemplo completos"""
    
    print("🚀 Inicializando base de datos...")
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    # Crear sesión
    db = SessionLocal()
    
    try:
        # Verificar si ya hay datos
        if db.query(Persona).count() > 0:
            print("⚠️  La base de datos ya contiene datos.")
            respuesta = input("¿Desea reinicializar? Esto eliminará todos los datos (s/n): ")
            if respuesta.lower() != 's':
                print("Operación cancelada.")
                return
            
            # Eliminar datos existentes
            print("🗑️  Eliminando datos existentes...")
            db.query(Reserva).delete()
            db.query(Articulo).delete()
            db.query(Sala).delete()
            db.query(Persona).delete()
            db.commit()
        
        print("\n👥 Creando usuarios...")
        
        # Crear admin principal
        admin = Persona(
            nombre="Admin Sistema",
            email="admin@sistema.com",
            telefono="+5491112345678",
            password_hash=pwd_context.hash("admin123"),
            rol="admin"
        )
        db.add(admin)
        print("  ✓ Admin creado (admin@sistema.com / admin123)")
        
        # Crear usuarios de prueba
        usuarios = []
        nombres_usuarios = [
            ("Ana", "Pérez", "ana.perez@empresa.com"),
            ("Juan", "Gómez", "juan.gomez@empresa.com"),
            ("María", "López", "maria.lopez@empresa.com"),
            ("Carlos", "Rodríguez", "carlos.rodriguez@empresa.com"),
            ("Luis", "Martínez", "luis.martinez@empresa.com"),
            ("Sofia", "Fernández", "sofia.fernandez@empresa.com"),
            ("Diego", "Sánchez", "diego.sanchez@empresa.com"),
            ("Laura", "Romero", "laura.romero@empresa.com"),
        ]
        
        for nombre, apellido, email in nombres_usuarios:
            usuario = Persona(
                nombre=f"{nombre} {apellido}",
                email=email,
                telefono=f"+54911{random.randint(10000000, 99999999)}",
                password_hash=pwd_context.hash("user123"),
                rol="usuario"
            )
            db.add(usuario)
            usuarios.append(usuario)
            print(f"  ✓ Usuario: {nombre} {apellido}")
        
        db.commit()
        usuarios.insert(0, admin)  # Agregar admin a la lista
        
        # Crear salas
        print("\n🏢 Creando salas...")
        salas_data = [
            ("Sala Ejecutiva", "Sala para reuniones ejecutivas con equipamiento premium", 10, True, True),
            ("Sala de Conferencias A", "Sala grande con proyector y sistema de audio", 20, True, True),
            ("Sala de Conferencias B", "Sala mediana para presentaciones", 15, True, False),
            ("Sala de Reuniones 1", "Sala pequeña para equipos de trabajo", 6, False, True),
            ("Sala de Reuniones 2", "Sala pequeña para reuniones rápidas", 6, False, False),
            ("Sala de Capacitación", "Sala equipada para sesiones de training", 25, True, True),
            ("Sala Innovación", "Espacio colaborativo con pizarras", 12, False, True),
        ]
        
        salas = []
        for nombre, desc, capacidad, proyector, pizarra in salas_data:
            sala = Sala(
                nombre=nombre,
                descripcion=desc,
                capacidad=capacidad,
                tiene_proyector=proyector,
                tiene_pizarra=pizarra
            )
            db.add(sala)
            salas.append(sala)
            print(f"  ✓ Sala: {nombre}")
        
        db.commit()
        
        # Crear artículos
        print("\n📦 Creando artículos...")
        articulos_data = [
            ("Proyector Epson EB-X05", "Proyector XGA 3.300 lúmenes", 5),
            ("Laptop HP EliteBook", "Laptop 14'' Intel i5 para presentaciones", 3),
            ("Cámara Sony Alpha", "Cámara mirrorless 24MP", 2),
            ("Pizarra Portátil", "Pizarra blanca con ruedas", 10),
            ("Marcadores", "Set de marcadores de colores", 20),
            ("Cable HDMI", "Cable HDMI 2.0 de 2m", 15),
            ("Adaptador VGA", "Adaptador VGA a HDMI", 8),
            ("Micrófono Inalámbrico", "Micrófono de solapa", 4),
            ("Parlantes Bluetooth", "Parlantes portátiles", 6),
            ("Extensión Eléctrica", "Zapatilla 6 tomas", 12),
        ]
        
        articulos = []
        for nombre, desc, stock in articulos_data:
            articulo = Articulo(
                nombre=nombre,
                descripcion=desc,
                stock=stock
            )
            db.add(articulo)
            articulos.append(articulo)
            print(f"  ✓ Artículo: {nombre} (Stock: {stock})")
        
        db.commit()
        
        # Generar reservas históricas (últimos 90 días)
        print("\n📅 Generando reservas históricas...")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        
        reservas_creadas = 0
        dias_laborables = [0, 1, 2, 3, 4]  # Lunes a Viernes
        horas_populares = [9, 10, 11, 14, 15, 16, 17]
        propositos = [
            "Reunión de equipo",
            "Presentación de proyecto",
            "Capacitación",
            "Entrevista",
            "Workshop",
            "Planificación estratégica",
            "Revisión de proyecto",
            "Sesión de brainstorming",
            "Reunión con cliente",
            "Demo de producto",
            "Sprint planning",
            "Retrospectiva"
        ]
        
        current_date = start_date
        while current_date < end_date:
            # Más reservas en días laborables
            if current_date.weekday() in dias_laborables:
                num_reservas_dia = random.randint(4, 10)
            else:
                num_reservas_dia = random.randint(0, 3)
            
            for _ in range(num_reservas_dia):
                sala = random.choice(salas)
                usuario = random.choice(usuarios)
                
                # Hora de inicio (más probable en horas populares)
                if random.random() < 0.7:
                    hora_inicio = random.choice(horas_populares)
                else:
                    hora_inicio = random.randint(8, 18)
                
                # Duración (1-4 horas)
                duracion = random.choice([1, 1, 2, 2, 3, 4])
                
                fecha_inicio = current_date.replace(
                    hour=hora_inicio,
                    minute=random.choice([0, 30]),
                    second=0,
                    microsecond=0
                )
                fecha_fin = fecha_inicio + timedelta(hours=duracion)
                
                # Verificar conflictos
                conflicto = db.query(Reserva).filter(
                    Reserva.sala_id == sala.id,
                    Reserva.fecha_inicio < fecha_fin,
                    Reserva.fecha_fin > fecha_inicio
                ).first()
                
                if not conflicto:
                    reserva = Reserva(
                        sala_id=sala.id,
                        persona_id=usuario.id,
                        fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin,
                        proposito=random.choice(propositos)
                    )
                    db.add(reserva)
                    reservas_creadas += 1
                    
                    # Asociar artículos (60% de las reservas)
                    if random.random() < 0.6 and articulos:
                        num_articulos = random.randint(1, 3)
                        articulos_reserva = random.sample(
                            articulos,
                            min(num_articulos, len(articulos))
                        )
                        for articulo in articulos_reserva:
                            reserva.articulos.append(articulo)
            
            # Commit periódico
            if reservas_creadas % 50 == 0 and reservas_creadas > 0:
                db.commit()
                print(f"  ⏳ {reservas_creadas} reservas creadas...")
            
            current_date += timedelta(days=1)
        
        db.commit()
        print(f"  ✓ {reservas_creadas} reservas históricas creadas")
        
        # Generar reservas futuras
        print("\n📆 Generando reservas futuras...")
        reservas_futuras = 0
        future_date = end_date + timedelta(days=1)
        
        for i in range(20):
            fecha = future_date + timedelta(days=random.randint(0, 45))
            if fecha.weekday() in dias_laborables:
                sala = random.choice(salas)
                usuario = random.choice(usuarios)
                hora_inicio = random.choice(horas_populares)
                duracion = random.choice([1, 2, 3])
                
                fecha_inicio = fecha.replace(
                    hour=hora_inicio,
                    minute=random.choice([0, 30]),
                    second=0,
                    microsecond=0
                )
                fecha_fin = fecha_inicio + timedelta(hours=duracion)
                
                # Verificar conflictos
                conflicto = db.query(Reserva).filter(
                    Reserva.sala_id == sala.id,
                    Reserva.fecha_inicio < fecha_fin,
                    Reserva.fecha_fin > fecha_inicio
                ).first()
                
                if not conflicto:
                    reserva = Reserva(
                        sala_id=sala.id,
                        persona_id=usuario.id,
                        fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin,
                        proposito=random.choice([
                            "Reunión planificada",
                            "Presentación importante",
                            "Training session",
                            "Revisión trimestral"
                        ])
                    )
                    db.add(reserva)
                    reservas_futuras += 1
        
        db.commit()
        print(f"  ✓ {reservas_futuras} reservas futuras creadas")
        
        # Resumen final
        print("\n" + "="*60)
        print("✅ BASE DE DATOS INICIALIZADA EXITOSAMENTE")
        print("="*60)
        print(f"👥 Usuarios: {len(usuarios)} (1 admin + {len(usuarios)-1} usuarios)")
        print(f"🏢 Salas: {len(salas)}")
        print(f"📦 Artículos: {len(articulos)}")
        print(f"📅 Reservas históricas: {reservas_creadas}")
        print(f"📆 Reservas futuras: {reservas_futuras}")
        print(f"📊 Total reservas: {reservas_creadas + reservas_futuras}")
        print("="*60)
        print("\n💡 CREDENCIALES DE ACCESO:")
        print("   👑 Admin:")
        print("      Email: admin@sistema.com")
        print("      Password: admin123")
        print("\n   👤 Usuarios de prueba:")
        print("      Email: ana.perez@empresa.com (y otros)")
        print("      Password: user123")
        print("="*60)
        
    except SQLAlchemyError as e:
        db.rollback()
        print(f"\n❌ Error al inicializar la base de datos: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
