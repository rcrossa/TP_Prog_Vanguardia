# Carpeta de Migraciones

Esta carpeta está preparada para futuras migraciones de base de datos con Alembic, pero **no es necesaria** para el funcionamiento actual del proyecto.

## Para este proyecto universitario:

✅ **Método actual (suficiente):**
```python
# En main.py
Base.metadata.create_all(bind=engine)
```

## Si en el futuro quisieras usar migraciones:

1. Instalar y configurar Alembic
2. Crear migración inicial
3. Reemplazar `create_all()` por `alembic upgrade head`

**Para este trabajo final, la carpeta puede permanecer vacía.**