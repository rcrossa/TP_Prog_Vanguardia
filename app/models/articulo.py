from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class Articulo(Base):
    __tablename__ = "articulos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    disponible = Column(Boolean, nullable=False)

    # Relación con reservas
    reservas = relationship("Reserva", back_populates="articulo")

    def __repr__(self):
        return f"<Articulo(id={self.id}, nombre='{self.nombre}', disponible={self.disponible})>"