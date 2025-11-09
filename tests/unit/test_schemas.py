"""
Pruebas unitarias para los esquemas Pydantic.
"""
import pytest
from pydantic import ValidationError
from app.schemas.persona import PersonaCreate, Persona
from app.schemas.sala import SalaCreate, Sala


class TestPersonaSchemas:
    """Pruebas para los esquemas de Persona."""

    def test_persona_create_valid(self):
        """Verifica la creación de PersonaCreate con datos válidos."""
        data = {
            "nombre": "Juan",
            "apellido": "Pérez",
            "email": "juan@example.com",
            "password": "password123",
            "is_admin": False,
            "is_active": True
        }
        persona = PersonaCreate(**data)

        assert persona.nombre == "Juan"
        assert persona.apellido == "Pérez"
        assert persona.email == "juan@example.com"
        assert persona.is_admin is False

    def test_persona_create_missing_required_fields(self):
        """Verifica que falla sin campos requeridos."""
        with pytest.raises(ValidationError):
            PersonaCreate(nombre="Juan", apellido="Pérez")  # Falta email y password

    def test_persona_response_valid(self):
        """Verifica Persona schema con datos válidos."""
        data = {
            "id": 1,
            "nombre": "María",
            "apellido": "García",
            "email": "maria@example.com",
            "is_admin": False,
            "is_active": True
        }

        persona = Persona(**data)

        assert persona.id == 1
        assert persona.nombre == "María"
        assert persona.email == "maria@example.com"


class TestSalaSchemas:
    """Pruebas para los esquemas de Sala."""

    def test_sala_create_valid(self):
        """Verifica la creación de SalaCreate con datos válidos."""
        data = {
            "nombre": "Sala Principal",
            "capacidad": 30,
            "disponible": True,
            "ubicacion": "Piso 1",
            "descripcion": "Sala grande"
        }

        sala = SalaCreate(**data)

        assert sala.nombre == "Sala Principal"
        assert sala.capacidad == 30
        assert sala.disponible is True

    def test_sala_create_invalid_capacidad(self):
        """Verifica validación de capacidad negativa."""
        data = {
            "nombre": "Sala Test",
            "capacidad": -5,  # Capacidad inválida
            "disponible": True
        }

        # La validación debe fallar con capacidad negativa
        with pytest.raises(ValidationError):
            SalaCreate(**data)

    def test_sala_response_valid(self):
        """Verifica Sala schema con datos válidos."""
        data = {
            "id": 1,
            "nombre": "Sala A",
            "capacidad": 20,
            "disponible": True,
            "ubicacion": "Piso 2",
            "descripcion": "Descripción"
        }

        sala = Sala(**data)

        assert sala.id == 1
        assert sala.nombre == "Sala A"
        assert sala.capacidad == 20
