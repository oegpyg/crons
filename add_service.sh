#!/bin/bash
# Script de ejemplo para agregar un nuevo servicio

# Este script muestra la estructura necesaria para agregar un servicio
# Cambiar "mi_servicio" por el nombre real del servicio

SERVICE_NAME="mi_servicio"
SERVICE_PREFIX="MI_SERVICIO"

# 1. Crear estructura de directorios
echo "1️⃣  Creando estructura de directorios..."
mkdir -p "src/services/$SERVICE_NAME"

# 2. Crear archivos de plantilla
echo "2️⃣  Creando archivos del servicio..."

cat > "src/services/$SERVICE_NAME/__init__.py" << 'EOF'
"""
Servicio personalizado - Descripción aquí.
"""

from .service import MiServicio

__all__ = ['MiServicio']
EOF

cat > "src/services/$SERVICE_NAME/service.py" << 'EOF'
"""
Implementación del servicio personalizado.
"""

import logging
from ..base_service import BaseService

logger = logging.getLogger(__name__)


class MiServicio(BaseService):
    """
    Servicio personalizado.
    
    Configuración requerida en .env (ejemplo con prefijo MI_SERVICIO_):
        MI_SERVICIO_ENABLED=true
        MI_SERVICIO_PARAM1=valor1
        MI_SERVICIO_PARAM2=valor2
        MI_SERVICIO_SCHEDULE_HOUR=9
        MI_SERVICIO_SCHEDULE_MINUTE=0
    """
    
    name = 'mi_servicio'
    schedule = {
        'hour': 9,
        'minute': 0,
        'timezone': 'America/Mexico_City'
    }
    
    def _validate_config(self):
        """Valida que la configuración tenga los campos requeridos."""
        required = ['param1', 'param2']
        missing = [key for key in required if key not in self.config]
        if missing:
            raise ValueError(f"Configuración incompleta. Faltan: {missing}")
    
    def execute(self) -> bool:
        """Ejecuta la lógica del servicio."""
        try:
            self.logger.info(f"Ejecutando {self.name}...")
            
            # Tu lógica aquí
            param1 = self.config.get('param1')
            param2 = self.config.get('param2')
            
            self.logger.info(f"Parámetro 1: {param1}")
            self.logger.info(f"Parámetro 2: {param2}")
            
            return True
        
        except Exception as e:
            self.logger.error(f"Error: {e}", exc_info=True)
            return False
EOF

echo "✅ Archivos creados en: src/services/$SERVICE_NAME/"

echo ""
echo "3️⃣  Próximos pasos:"
echo "   a) Editar src/main.py - agregar en load_services():"
echo "      from services.$SERVICE_NAME import MiServicio"
echo "      service = MiServicio.from_env('${SERVICE_PREFIX}_', self.env_vars)"
echo ""
echo "   b) Editar .env y agregar:"
echo "      ${SERVICE_PREFIX}_ENABLED=true"
echo "      ${SERVICE_PREFIX}_PARAM1=valor1"
echo "      ${SERVICE_PREFIX}_PARAM2=valor2"
echo ""
echo "   c) Ver ARCHITECTURE.md para más detalles"
echo ""
echo "🎉 Listo para personalizador"
