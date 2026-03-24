"""
EJEMPLO: Segundo Servicio - Recordatorios de Vencimientos

Este archivo muestra cómo se implementaría un segundo servicio
en la arquitectura modular. Puedes usarlo como plantilla.
"""

from ..base_service import BaseService
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# ARCHIVO: src/services/expiry_reminder/__init__.py
# ============================================================================

"""
__init__.py - Exposer la clase del servicio

from .service import ExpiryReminderService
__all__ = ['ExpiryReminderService']
"""


# ============================================================================
# ARCHIVO: src/services/expiry_reminder/service.py
# ============================================================================

class ExpiryReminderService(BaseService):
    """
    Servicio que verifica vencimientos y envía recordatorios.
    
    Configuración en .env:
        EXPIRY_ENABLED=true
        EXPIRY_DB_HOST=mysql.example.com
        EXPIRY_DB_PORT=3306
        EXPIRY_DB_USER=user
        EXPIRY_DB_PASSWORD=pass
        EXPIRY_DB_NAME=contracts
        EXPIRY_CHECK_DAYS_BEFORE=30
        EXPIRY_NOTIFICATIONS_API_URL=http://api:8888
        EXPIRY_BOT_ID=2
        EXPIRY_CHAT_ID=987654321
        EXPIRY_SCHEDULE_HOUR=8
        EXPIRY_SCHEDULE_MINUTE=0
    """
    
    name = 'expiry_reminder'
    schedule = {
        'hour': 8,
        'minute': 0,
        'timezone': 'America/Mexico_City'
    }
    
    def _validate_config(self):
        """Valida configuración específica."""
        required = [
            'db_host', 'db_port', 'db_user', 'db_password', 'db_name',
            'notifications_api_url', 'bot_id', 'chat_id', 'check_days_before'
        ]
        missing = [k for k in required if k not in self.config]
        if missing:
            raise ValueError(f"Faltan: {missing}")
    
    def execute(self) -> bool:
        """Verifica vencimientos y envía notificaciones."""
        try:
            self.logger.info("Verificando vencimientos...")
            
            # 1. Conectar a BD
            # 2. Buscar contratos que vencen en X días
            # 3. Enviar notificaciones
            
            return True
        except Exception as e:
            self.logger.error(f"Error: {e}", exc_info=True)
            return False


# ============================================================================
# ARCHIVO: src/main.py - EN load_services()
# ============================================================================

"""
def load_services(self):
    logger.info("Cargando servicios...")
    
    # Servicio 1: Cumpleaños
    try:
        from services.birthday import BirthdayService
        service = BirthdayService.from_env('BIRTHDAY_', self.env_vars)
        if service:
            self.services.append(service)
            logger.info(f"✅ Servicio cargado: {service.name}")
    except Exception as e:
        logger.error(f"❌ Error cargando Birthday: {e}")
    
    # NUEVO: Servicio 2: Vencimientos
    try:
        from services.expiry_reminder import ExpiryReminderService
        service = ExpiryReminderService.from_env('EXPIRY_', self.env_vars)
        if service:
            self.services.append(service)
            logger.info(f"✅ Servicio cargado: {service.name}")
    except Exception as e:
        logger.error(f"❌ Error cargando Expiry Reminder: {e}")
    
    # Se pueden agregar más servicios siguiendo el mismo patrón
"""


# ============================================================================
# ARCHIVO: .env - NUEVA SECCIÓN
# ============================================================================

"""
# ============================================================
# SERVICIO 2: RECORDADOR DE VENCIMIENTOS
# ============================================================

EXPIRY_ENABLED=true
EXPIRY_DB_HOST=mysql.example.com
EXPIRY_DB_PORT=3306
EXPIRY_DB_USER=usuario
EXPIRY_DB_PASSWORD=password
EXPIRY_DB_NAME=contracts
EXPIRY_CHECK_DAYS_BEFORE=30
EXPIRY_NOTIFICATIONS_API_URL=http://api:8888
EXPIRY_BOT_ID=2
EXPIRY_CHAT_ID=987654321
EXPIRY_SCHEDULE_HOUR=8
EXPIRY_SCHEDULE_MINUTE=0
"""


# ============================================================================
# VENTAJAS DE ESTE DISEÑO
# ============================================================================

"""
✅ Cada servicio es completamente independiente
✅ Pueden usar diferentes BDs, APIs, horarios
✅ Cambiar un servicio no afecta otros
✅ Configuración descentralizada en .env
✅ Fácil agregar/remover servicios
✅ Testing aislado por servicio
✅ Escalable a N servicios
✅ Sin modificar lógica base
"""
