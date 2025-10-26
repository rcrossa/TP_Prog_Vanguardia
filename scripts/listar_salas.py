"""Script para listar todas las salas en la base de datos."""
from app.core.database import SessionLocal
from app.models.sala import Sala

def listar_salas():
    """Listar todas las salas en la base de datos e imprimir sus detalles."""
    db = SessionLocal()
    salas = db.query(Sala).all()
    print("Salas en la base de datos:")
    for sala in salas:
        print(f"ID: {sala.id}, Nombre: {sala.nombre}, "
              f"Capacidad: {sala.capacidad}, Disponible: {sala.disponible}")
    db.close()

if __name__ == "__main__":
    listar_salas()
