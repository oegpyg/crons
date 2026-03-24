"""
Clase base para todos los servicios de cron.
Define la interfaz que debe implementar cada servicio.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


logger = logging.getLogger(__name__)


class BaseService(ABC):
    """
    Clase base para todos los servicios de cron.
    
    Cada servicio debe:
    1. Heredar de BaseService
    2. Implementar execute()
    3. Definir name, schedule y default_config
    """
    
    name: str                          # Nombre único del servicio
    schedule: Dict[str, Any] = {}      # {'hour': 6, 'minute': 0, 'timezone': '...'}
    enabled: bool = True               # Si está habilitado
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa el servicio con su configuración específica.
        
        Args:
            config: Diccionario con la configuración del servicio desde .env
        """
        self.config = config
        self.logger = logging.getLogger(f"services.{self.name}")
        self._validate_config()
    
    def _validate_config(self):
        """
        Valida que la configuración tenga los campos requeridos.
        Cada servicio debe sobrescribir esto si es necesario.
        """
        pass
    
    @abstractmethod
    def execute(self) -> bool:
        """
        Ejecuta la lógica del servicio.
        
        Returns:
            bool: True si fue exitoso, False si hubo error
        """
        pass
    
    def run(self) -> None:
        """
        Envuelve la ejecución con logging y manejo de errores.
        Llamado automáticamente por el scheduler.
        """
        try:
            self.logger.info(f"Iniciando servicio: {self.name}")
            success = self.execute()
            
            if success:
                self.logger.info(f"✅ Servicio {self.name} completado exitosamente")
            else:
                self.logger.warning(f"⚠️  Servicio {self.name} completado con advertencias")
        
        except Exception as e:
            self.logger.error(f"❌ Error en servicio {self.name}: {e}", exc_info=True)
    
    @classmethod
    def from_env(cls, env_prefix: str, env_vars: Dict[str, str]) -> Optional['BaseService']:
        """
        Crea una instancia del servicio desde variables de entorno.
        
        Args:
            env_prefix: Prefijo para las variables (ej: "BIRTHDAY_")
            env_vars: Diccionario de variables de entorno
        
        Returns:
            Instancia del servicio o None si no está habilitado
        """
        # Verificar si está habilitado
        enabled_key = f"{env_prefix}ENABLED"
        if env_vars.get(enabled_key, 'false').lower() != 'true':
            return None
        
        # Extraer variables pour este servicio
        config = {}
        prefix_len = len(env_prefix)
        
        for key, value in env_vars.items():
            if key.startswith(env_prefix) and key != enabled_key:
                # Remover el prefijo para obtener el nombre real
                config_key = key[prefix_len:].lower()
                config[config_key] = value
        
        return cls(config)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, enabled={self.enabled})"
