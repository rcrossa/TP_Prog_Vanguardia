"""
Pruebas unitarias para el servicio de autenticación.
"""
from unittest.mock import Mock, patch
from app.services.auth_service import AuthService
from app.models.persona import Persona
from app.auth.jwt_handler import get_password_hash, verify_password


class TestAuthService:
    """Pruebas para el servicio de autenticación."""

    def test_password_hashing(self):
        """Verifica que el hash de contraseña funciona correctamente."""
        password = "mi_password_seguro_123"
        hashed = get_password_hash(password)

        # El hash no debe ser igual a la contraseña original
        assert hashed != password
        # El hash debe tener contenido
        assert len(hashed) > 0
        # Verificar que la contraseña coincide con el hash
        assert verify_password(password, hashed) is True

    def test_password_verification_fails_with_wrong_password(self):
        """Verifica que la verificación falla con contraseña incorrecta."""
        password = "password_correcto"
        wrong_password = "password_incorrecto"
        hashed = get_password_hash(password)

        # La verificación debe fallar
        assert verify_password(wrong_password, hashed) is False

    def test_authenticate_user_success(self):
        """Verifica autenticación exitosa de usuario."""
        # Crear mock de la base de datos
        mock_db = Mock()

        # Crear usuario de prueba con contraseña hasheada
        test_password = "test123"
        test_user = Persona(
            id=1,
            nombre="Test",
            email="test@example.com",
            hashed_password=get_password_hash(test_password),
            is_active=True
        )

        # Mock del repositorio para devolver el usuario
        with patch(
            'app.services.auth_service.PersonaRepository.get_by_email',
            return_value=test_user
        ):
            result = AuthService.authenticate_user(
                mock_db,
                "test@example.com",
                test_password
            )

            assert result is not None
            assert result.email == "test@example.com"

    def test_authenticate_user_wrong_password(self):
        """Verifica que falla autenticación con contraseña incorrecta."""
        mock_db = Mock()

        test_user = Persona(
            id=1,
            nombre="Test",
            email="test@example.com",
            hashed_password=get_password_hash("correct_password"),
            is_active=True
        )

        with patch(
            'app.services.auth_service.PersonaRepository.get_by_email',
            return_value=test_user
        ):
            result = AuthService.authenticate_user(
                mock_db,
                "test@example.com",
                "wrong_password"
            )

            assert result is None

    def test_authenticate_user_not_found(self):
        """Verifica que falla autenticación cuando usuario no existe."""
        mock_db = Mock()

        with patch(
            'app.services.auth_service.PersonaRepository.get_by_email',
            return_value=None
        ):
            result = AuthService.authenticate_user(
                mock_db,
                "noexiste@example.com",
                "password"
            )

            assert result is None
