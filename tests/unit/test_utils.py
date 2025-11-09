"""
Pruebas unitarias para utilidades y funciones helper.
"""
from datetime import timedelta
from app.auth.jwt_handler import create_access_token, verify_password, get_password_hash


class TestJWTHandler:
    """Pruebas para el manejador de JWT."""

    def test_create_access_token(self):
        """Verifica la creación de tokens JWT."""
        data = {"sub": "test@example.com"}
        token = create_access_token(data)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_with_expiration(self):
        """Verifica la creación de tokens con tiempo de expiración."""
        data = {"sub": "test@example.com"}
        expires_delta = timedelta(minutes=30)

        token = create_access_token(data, expires_delta=expires_delta)

        assert token is not None
        assert isinstance(token, str)


class TestPasswordUtilities:
    """Pruebas para utilidades de contraseñas."""

    def test_password_hash_is_different(self):
        """Verifica que el hash sea diferente de la contraseña original."""
        password = "mi_password_123"
        hashed = get_password_hash(password)

        assert hashed != password
        assert len(hashed) > len(password)

    def test_same_password_different_hashes(self):
        """Verifica que la misma contraseña genera hashes diferentes."""
        password = "mismo_password"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        # Los hashes deben ser diferentes debido al salt
        assert hash1 != hash2
        # Pero ambos deben verificar correctamente
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True

    def test_verify_password_correct(self):
        """Verifica que la verificación funciona con contraseña correcta."""
        password = "test_password_456"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Verifica que la verificación falla con contraseña incorrecta."""
        password = "correct_password"
        wrong_password = "wrong_password"
        hashed = get_password_hash(password)

        assert verify_password(wrong_password, hashed) is False

    def test_verify_password_empty(self):
        """Verifica comportamiento con contraseña vacía."""
        password = ""
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True
        assert verify_password("not_empty", hashed) is False
