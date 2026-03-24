"""
Scheduler principal del sistema de crons.
Gestiona múltiples servicios, cada uno con su horario y configuración.
"""

import os
import sys
import logging
import time
from typing import Dict, List
from apscheduler.schedulers.background import BackgroundScheduler

from services.birthday import BirthdayService

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CronManager:
    """Gestor central de servicios de cron."""
    
    def __init__(self):
        """Inicializa el gestor de servicios."""
        self.services: List[object] = []
        self.scheduler = BackgroundScheduler()
        self.env_vars = os.environ.copy()
    
    def load_services(self):
        """
        Carga todos los servicios disponibles.
        Cada servicio se carga desde su configuración en .env.
        """
        logger.info("Cargando servicios...")
        
        # Cargar servicio de cumpleaños
        try:
            service = BirthdayService.from_env('BIRTHDAY_', self.env_vars)
            if service:
                self.services.append(service)
                logger.info(f"✅ Servicio cargado: {service.name}")
            else:
                logger.info("ℹ️  Servicio de cumpleaños deshabilitado")
        except Exception as e:
            logger.error(f"❌ Error cargando servicio de cumpleaños: {e}")
        
        # Aquí se pueden agregar más servicios:
        # - Cargar desde un directorio dinámicamente
        # - Usar un registry de servicios
        # - etc.
        
        if not self.services:
            logger.warning("⚠️  No hay servicios habilitados")
            return False
        
        logger.info(f"✅ Se cargaron {len(self.services)} servicio(s)")
        return True
    
    def schedule_services(self):
        """Programa cada servicio según su horario."""
        for service in self.services:
            try:
                schedule_config = service.schedule.copy()
                timezone = schedule_config.pop('timezone', 'UTC')
                
                self.scheduler.add_job(
                    service.run,
                    'cron',
                    timezone=timezone,
                    id=service.name,
                    **schedule_config
                )
                
                logger.info(
                    f"✅ Servicio '{service.name}' programado: "
                    f"{schedule_config.get('hour', '?')}:"
                    f"{str(schedule_config.get('minute', '0')).zfill(2)}"
                )
            except Exception as e:
                logger.error(f"❌ Error programando {service.name}: {e}")
    
    def start(self):
        """Inicia el scheduler y mantiene el proceso vivo."""
        try:
            if not self.load_services():
                logger.critical("No hay servicios para ejecutar")
                return 1
            
            self.schedule_services()
            
            self.scheduler.start()
            logger.info("🚀 Scheduler iniciado correctamente")
            
            # Ejecutar prueba inmediata del primer servicio (para verificar config)
            if self.services:
                logger.info("Ejecutando primer servicio como prueba...")
                self.services[0].run()
            
            # Mantener el proceso vivo
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Recibida señal de interrupción...")
                self.shutdown()
        
        except Exception as e:
            logger.error(f"❌ Error fatal: {e}", exc_info=True)
            return 1
    
    def shutdown(self):
        """Detiene el scheduler de forma ordenada."""
        logger.info("Deteniendo scheduler...")
        if self.scheduler.running:
            self.scheduler.shutdown()
        logger.info("✅ Scheduler detenido")


def main():
    """Función principal."""
    logger.info("="*60)
    logger.info("SISTEMA DE CRONS - NOTIFICACIONES")
    logger.info("="*60)
    
    manager = CronManager()
    return manager.start()


if __name__ == '__main__':
    sys.exit(main() or 0)
