#!/usr/bin/env python3
"""
Script para crear un usuario administrador inicial.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.persona import PersonaCreate
from app.services.persona_service import PersonaService

def create_admin_user():
    """Crear usuario administrador inicial."""
    db_gen = get_db()
    db: Session = next(db_gen)
    
    try:
        # Datos del admin
        admin_data = PersonaCreate(
            nombre="Admin Usuario",
            email="admin@test.com",
            password="admin123",
            is_admin=True,
            is_active=True
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
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creando usuario admin: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()