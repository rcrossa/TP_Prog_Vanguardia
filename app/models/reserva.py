from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_articulo = Column(Integer, ForeignKey("articulos.id"), nullable=True)
    id_sala = Column(Integer, ForeignKey("salas.id"), nullable=True)
    id_persona = Column(Integer, ForeignKey("personas.id"), nullable=False)
    fecha_hora_inicio = Column(DateTime, nullable=False)
    fecha_hora_fin = Column(DateTime, nullable=False)

    # Relaciones
    persona = relationship("Persona", back_populates="reservas")
    articulo = relationship("Articulo", back_populates="reservas")
    sala = relationship("Sala", back_populates="reservas")

    def __repr__(self):
        return (f"<Reserva(id={self.id}, id_persona={self.id_persona}, "
                f"id_articulo={self.id_articulo}, id_sala={self.id_sala}, "
                f"inicio='{self.fecha_hora_inicio}', fin='{self.fecha_hora_fin}')>")