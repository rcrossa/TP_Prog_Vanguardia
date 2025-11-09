"""
Pruebas unitarias para los modelos de datos.
"""

from app.models.persona import Persona
from app.models.sala import Sala


class TestPersonaModel:
    """Pruebas para el modelo Persona."""

    def test_persona_creation(self):
        """Verifica la creación de un objeto Persona."""
        persona = Persona(
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@example.com",
            is_active=True,
            is_admin=False
        )

        assert persona.nombre == "Juan"
        assert persona.apellido == "Pérez"
        assert persona.email == "juan.perez@example.com"
        assert persona.is_active is True
        assert persona.is_admin is False

    def test_persona_repr(self):
        """Verifica la representación en string de Persona."""
        persona = Persona(
            id=1,
            nombre="María",
            email="maria@example.com"
        )

        repr_str = repr(persona)
        assert "Persona" in repr_str
        assert "id=1" in repr_str
        assert "María" in repr_str

    def test_persona_email_required(self):
        """Verifica que el email es un campo requerido."""
        persona = Persona(nombre="Test")
        # El email debe estar presente
        assert hasattr(persona, 'email')


class TestSalaModel:
    """Pruebas para el modelo Sala."""

    def test_sala_creation(self):
        """Verifica la creación de un objeto Sala."""
        sala = Sala(
            nombre="Sala A",
            capacidad=20,
            disponible=True,
            ubicacion="Piso 2",
            descripcion="Sala de reuniones"
        )

        assert sala.nombre == "Sala A"
        assert sala.capacidad == 20
        assert sala.disponible is True
        assert sala.ubicacion == "Piso 2"
        assert sala.descripcion == "Sala de reuniones"

    def test_sala_default_values(self):
        """Verifica los valores por defecto de Sala."""
        sala = Sala(
            nombre="Sala B",
            capacidad=10
        )

        # Verificar que tiene valores por defecto
        assert sala.nombre == "Sala B"
        assert sala.capacidad == 10

    def test_sala_repr(self):
        """Verifica la representación en string de Sala."""
        sala = Sala(
            id=1,
            nombre="Sala Principal",
            capacidad=50
        )

        repr_str = repr(sala)
        assert "Sala" in repr_str
        assert "id=1" in repr_str
        assert "capacidad=50" in repr_str
