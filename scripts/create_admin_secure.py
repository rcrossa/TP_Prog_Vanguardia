#!/usr/bin/env python3
"""
Script SEGURO para crear un usuario administrador inicial.

✅ Este script usa variables de entorno o prompts interactivos.
✅ Apto para desarrollo Y producción.

Uso:
    1. Con variables de entorno:
       export ADMIN_NAME="Admin Usuario"
       export ADMIN_EMAIL="admin@example.com"
       export ADMIN_PASSWORD="tu_contraseña_segura"
       python scripts/create_admin_secure.py

    2. Modo interactivo (sin variables de entorno):
       python scripts/create_admin_secure.py
       # Te pedirá ingresar los datos manualmente
"""
import getpass
import os
import sys

# Ajustar el path para importar desde la raíz del proyecto
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.persona import PersonaCreate
from app.services.persona_service import PersonaService


def get_admin_credentials():
    """
    Obtener credenciales del admin de forma segura.
    Primero intenta variables de entorno, luego prompt interactivo.
    """
    # Intentar obtener de variables de entorno
    nombre = os.getenv("ADMIN_NAME")
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")

    # Si no están las variables de entorno, pedirlas interactivamente
    if not all([nombre, email, password]):
        print("📝 Variables de entorno no encontradas. Ingrese datos manualmente:")
        print()

        if not nombre:
            nombre = input("Nombre del administrador: ").strip()

        if not email:
            email = input("Email del administrador: ").strip()

        if not password:
            password = getpass.getpass("Contraseña del administrador: ")
            password_confirm = getpass.getpass("Confirme la contraseña: ")

            if password != password_confirm:
                print("❌ Las contraseñas no coinciden.")
                sys.exit(1)

    # Validar que no estén vacías
    if not all([nombre, email, password]):
        print("❌ Error: Todos los campos son obligatorios.")
        sys.exit(1)

    # Advertencia si se usa una contraseña débil
    if len(password) < 8:
        print("⚠️  ADVERTENCIA: La contraseña es muy corta (menos de 8 caracteres)")
        confirmar = input("¿Continuar de todos modos? (s/N): ").strip().lower()
        if confirmar != "s":
            print("❌ Operación cancelada.")
            sys.exit(1)

    return nombre, email, password


def create_admin_user():
    """
    Crear usuario administrador inicial de forma segura.
    """
    print("🔧 Creando usuario administrador...")
    print()

    # Obtener credenciales de forma segura
    nombre, email, password = get_admin_credentials()

    db_gen = get_db()
    db: Session = next(db_gen)

    try:
        # Crear datos del admin
        admin_data = PersonaCreate(
            nombre=nombre, email=email, password=password, is_admin=True, is_active=True
        )

        # Verificar si ya existe
        from app.repositories.persona_repository import PersonaRepository

        existing_admin = PersonaRepository.get_by_email(db, admin_data.email)

        if existing_admin:
            print(f"✅ El usuario admin ya existe: {existing_admin.email}")
            print(f"   ID: {existing_admin.id}")
            print(f"   Nombre: {existing_admin.nombre}")
            print(f"   Es admin: {existing_admin.is_admin}")
            print(f"   Está activo: {existing_admin.is_active}")
            print()
            print(
                "💡 Tip: Si quieres actualizar la contraseña, elimina el usuario primero."
            )
            return existing_admin

        # Crear el admin
        admin_user = PersonaService.create_persona(db, admin_data)
        db.commit()

        print()
        print("🎉 Usuario administrador creado exitosamente!")
        print(f"   Email: {admin_user.email}")
        print(f"   ID: {admin_user.id}")
        print(f"   Nombre: {admin_user.nombre}")
        print()
        print("✅ Ahora puedes iniciar sesión con estas credenciales.")

        return admin_user

    except Exception as e:
        db.rollback()
        print(f"❌ Error creando usuario admin: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    try:
        create_admin_user()
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario.")
        sys.exit(1)
