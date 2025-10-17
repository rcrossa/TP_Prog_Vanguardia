"""
Paquete web para la interfaz de usuario.

Este paquete contiene los routers y controladores para
servir las páginas web del sistema.
"""

from .routes import router as web_router

__all__ = ["web_router"]
