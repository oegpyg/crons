"""
Servicio de notificaciones de cumpleaños.
Consulta una BD MySQL para encontrar cumpleaños de hoy
y envía notificaciones a una API.
"""

from .service import BirthdayService

__all__ = ['BirthdayService']
