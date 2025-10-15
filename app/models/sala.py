from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Sala(Base):
    __tablename__ = "salas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    capacidad = Column(Integer, nullable=False)

    # Relación con reservas
    reservas = relationship("Reserva", back_populates="sala")

    def __repr__(self):
        return f"<Sala(id={self.id}, nombre='{self.nombre}', capacidad={self.capacidad})>"