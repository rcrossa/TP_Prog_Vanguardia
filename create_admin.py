#!/usr/bin/env python3
"""
Script para crear un usuario administrador inicial.

⚠️  ADVERTENCIA DE SEGURIDAD:
    Este script contiene credenciales hardcodeadas y es SOLO para DESARROLLO/TESTING.

    ❌ NO USAR EN PRODUCCIÓN
    ❌ Las credenciales aquí son de ejemplo y deben cambiarse

    Para producción, usar variables de entorno o prompts seguros.
    Ver: create_admin_secure.py para una versión más segura.
"""


import os
import sys
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.persona import PersonaCreate
from app.services.persona_service import PersonaService
from app.repositories.persona_repository import PersonaRepository
from app.core import config

# Ajustar el path para importar desde la raíz del proyecto
import pathlib
project_root = pathlib.Path(__file__).parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def create_admin_user():
    """
    Crear usuario administrador inicial.

    ⚠️  SOLO PARA DESARROLLO - Credenciales hardcodeadas
    """
    # Detectar si estamos en Docker
    def running_in_docker():
        # Docker crea este archivo en los contenedores Linux
        return os.path.exists('/.dockerenv') or os.getenv('DOCKER_CONTAINER', '') == 'true'

    # Ajustar el host automáticamente
    if running_in_docker():
        os.environ['POSTGRES_HOST'] = 'postgres'
    else:
        os.environ['POSTGRES_HOST'] = os.getenv('POSTGRES_HOST', 'localhost')

    # Forzar recarga de settings
    config.settings.postgres_host = os.environ['POSTGRES_HOST']

    db_gen = get_db()
    db: Session = next(db_gen)

    try:
        # ⚠️  CREDENCIALES DE DESARROLLO - NO USAR EN PRODUCCIÓN
        admin_data = PersonaCreate(
            nombre="Admin Usuario",
            apellido="Admin",
            email="admin@test.com",
            password="admin123",  # ⚠️  Contraseña de ejemplo
            is_admin=True,
            is_active=True,
        )

        # Verificar si ya existe

        existing_admin = PersonaRepository.get_by_email(db, admin_data.email)

        if existing_admin:
            print(f"✅ El usuario admin ya existe: {existing_admin.email}")
            print(f"   ID: {existing_admin.id}")
            print(f"   Nombre: {existing_admin.nombre}")
            print(f"   Es admin: {existing_admin.is_admin}")
            print(f"   Está activo: {existing_admin.is_active}")
            return existing_admin

        # Crear el admin
        admin_user = PersonaService.create_persona(db, admin_data)
        db.commit()

        print("🎉 Usuario administrador creado exitosamente!")
        print(f"   Email: {admin_user.email}")
        print(f"   Password: admin123")
        print(f"   ID: {admin_user.id}")
        print(f"   Nombre: {admin_user.nombre}")

        return admin_user
    except Exception as exc:
        db.rollback()
        print(f"❌ Error creando usuario admin: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_admin_user()
