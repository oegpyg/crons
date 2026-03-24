"""
Módulo de servicios para el sistema de crons.
Cada servicio es una unidad independiente que puede ser:
- Habilitado/deshabilitado desde .env
- Configurado de manera específica
- Ejecutado en su propio horario
"""

from .base_service import BaseService

__all__ = ['BaseService']
