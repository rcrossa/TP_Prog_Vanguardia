from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

    # Relación con reservas
    reservas = relationship("Reserva", back_populates="persona")

    def __repr__(self):
        return f"<Persona(id={self.id}, nombre='{self.nombre}', email='{self.email}')>"