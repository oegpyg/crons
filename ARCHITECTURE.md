# 🏗️ Arquitectura del Sistema Modular

## Visión General

Sistema extensible de servicios programados. Cada servicio es una unidad independiente que puede ser:
- Activada/desactivada desde `.env`
- Configurada con parámetros específicos
- Programada en su propio horario
- Extendida sin afectar otros servicios

```
┌──────────────────────────────────────────────┐
│         Docker Container                      │
│                                               │
│  ┌────────────────────────────────────────┐  │
│  │     CronManager (main.py)              │  │
│  │     - Carga servicios                  │  │
│  │     - Programa horarios                │  │
│  │     - Gestiona ciclo de vida           │  │
│  └────────────────────────────────────────┘  │
│           │                                   │
│    ┌──────┴───────┬────────────┐             │
│    ▼              ▼            ▼             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Birthday │  │ Servicio │  │ Servicio │  │
│  │ Service  │  │    2     │  │    3     │  │
│  └──┬───────┘  └──┬───────┘  └──┬───────┘  │
│     │             │             │          │
└─────┼─────────────┼─────────────┼──────────┘
      │             │             │
      ▼             ▼             ▼
   MySQL      Service #2      Service #3
   BD          Resources       Resources
```

## Componentes Principales

### 1. **CronManager** (main.py)
Gestor central de todos los servicios:
- Carga servicios disponibles desde `.env`
- Programa cada servicio según su horario
- Maneja ciclo de vida (start/shutdown)
- Proporciona logging centralizado

**Método key: `load_services()`**
```python
def load_services(self):
    # Cargar servicio de cumpleaños
    service = BirthdayService.from_env('BIRTHDAY_', self.env_vars)
    if service:
        self.services.append(service)
    
    # Se pueden agregar más servicios aquí
```

### 2. **BaseService** (base_service.py)
Clase abstracta base para todos los servicios:

```python
class BaseService(ABC):
    name: str                      # Nombre único
    schedule: Dict                 # {'hour': 6, 'minute': 0, ...}
    enabled: bool
    
    @abstractmethod
    def execute(self) -> bool      # Implementar lógica
    
    @classmethod
    def from_env(env_prefix, env_vars)  # Cargar desde .env
```

**Ventajas**:
- Interfaz estándar para todos los servicios
- Manejo automático de errores y logging
- Carga dinámica desde variables de entorno
- Validación de configuración

### 3. **Birthday Service**
Ejemplo de implementación de servicio:

```python
class BirthdayService(BaseService):
    name = 'birthday_notifier'
    schedule = {
        'hour': 6,
        'minute': 0,
        'timezone': 'America/Mexico_City'
    }
    
    def execute(self) -> bool:
        # 1. Conectar a BD MySQL
        # 2. Consultar cumpleaños
        # 3. Enviar notificaciones
        return True
```

**Carga desde .env**:
```env
BIRTHDAY_ENABLED=true
BIRTHDAY_DB_HOST=mysql.example.com
BIRTHDAY_DB_USER=usuario
BIRTHDAY_NOTIFICATIONS_API_URL=http://api:8888
BIRTHDAY_BOT_ID=1
BIRTHDAY_CHAT_ID=123456789
```

## Flujo de Ejecución

```
┌──────────────────────┐
│  main.py inicia      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────┐
│  CronManager.start()     │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  load_services()         │
│  - Lee .env              │
│  - Instancia servicios   │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  schedule_services()     │
│  - Programa horarios     │
│  - APScheduler comienza  │
└──────────┬───────────────┘
           │
    ┌──────┴──────────┐
    │                 │
    ▼                 ▼
 6:00 AM          9:00 AM
 Birthday         Servicio 2
 Service.run()    run()
    │                 │
    ▼                 ▼
 execute()         execute()
    │                 │
    └────────┬────────┘
             │
             ▼
         Logging
         Resultado
```

## Extensibilidad: Agregar un Nuevo Servicio

### Paso 1: Crear estructura
```bash
mkdir -p src/services/mi_servicio
touch src/services/mi_servicio/__init__.py
touch src/services/mi_servicio/service.py
```

### Paso 2: Implementar servicio

**src/services/mi_servicio/service.py**:
```python
from ..base_service import BaseService

class MiServicio(BaseService):
    name = 'mi_servicio'
    schedule = {
        'hour': 9,
        'minute': 0,
        'timezone': 'America/Mexico_City'
    }
    
    def _validate_config(self):
        required = ['param1', 'param2']
        missing = [k for k in required if k not in self.config]
        if missing:
            raise ValueError(f"Faltan: {missing}")
    
    def execute(self) -> bool:
        try:
            self.logger.info(f"Ejecutando {self.name}")
            # Tu lógica aquí
            return True
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return False
```

**src/services/mi_servicio/__init__.py**:
```python
from .service import MiServicio

__all__ = ['MiServicio']
```

### Paso 3: Registrar en main.py

En `src/main.py`, en el método `load_services()`:
```python
from services.mi_servicio import MiServicio

# ...

# Cargar nuevo servicio
try:
    service = MiServicio.from_env('MI_SERVICIO_', self.env_vars)
    if service:
        self.services.append(service)
        logger.info(f"✅ Servicio cargado: {service.name}")
except Exception as e:
    logger.error(f"❌ Error cargando MiServicio: {e}")
```

### Paso 4: Configurar en .env

```env
# Servicio personalizado
MI_SERVICIO_ENABLED=true
MI_SERVICIO_PARAM1=valor1
MI_SERVICIO_PARAM2=valor2
MI_SERVICIO_SCHEDULE_HOUR=9
MI_SERVICIO_SCHEDULE_MINUTE=30
```

## Manejo de Errores

Cada servicio tiene manejo automático de errores via `run()`:

```python
def run(self) -> None:
    try:
        self.logger.info(f"Iniciando: {self.name}")
        success = self.execute()
        
        if success:
            self.logger.info(f"✅ {self.name} completado")
        else:
            self.logger.warning(f"⚠️  {self.name} con advertencias")
    
    except Exception as e:
        self.logger.error(f"❌ Error en {self.name}: {e}")
```

**Niveles de log**:
- `INFO`: Operaciones normales
- `WARNING`: Problemas no críticos
- `ERROR`: Fallos en ejecución

## Estructura de Directorios

```
src/
├── main.py                         # Scheduler principal
├── services/
│   ├── __init__.py
│   ├── base_service.py             # Clase base
│   ├── birthday/
│   │   ├── __init__.py
│   │   └── service.py              # Birthday service
│   └── mi_servicio/                # Nuevo servicio (ejemplo)
│       ├── __init__.py
│       └── service.py
├── test_config.py                  # Tests
└── config.py                        # Config global (futuro)
```

## Carga Dinámica de Servicios

El sistema soporta carga dinámica y automática:

```python
# 1. Lee todas las variables de entorno
env_vars = os.environ.copy()

# 2. Para cada servicio disponible, intenta cargar
# 3. Si ENABLED=true, lo instancia
# 4. Si falla la validación, registra error y continúa
# 5. Los servicios activos se programan en el scheduler
```

## Variables de Entorno por Servicio

```env
# Convención: [SERVICIO_]VARIABLE=valor

# Servicio 1
BIRTHDAY_ENABLED=true
BIRTHDAY_DB_HOST=...
BIRTHDAY_NOTIFICATIONS_API_URL=...

# Servicio 2
OTRO_ENABLED=true
OTRO_CONFIG_X=...
OTRO_SCHEDULE_HOUR=9

# Global
TZ=America/Mexico_City
```

## Ventajas del Diseño Modular

✅ **Independencia**: Cada servicio funciona solo  
✅ **Extensibilidad**: Agregar servicios sin modificar existentes  
✅ **Configuración**: Cada servicio con sus propios parámetros  
✅ **Mantenibilidad**: Código organizado y limpio  
✅ **Testing**: Fácil de probar cada servicio  
✅ **Escalabilidad**: Soporta múltiples servicios simultáneos  

## Limitaciones y Futuro

### Posibles Mejoras:

1. **Registro de eventos**
   - Tabla en BD para historial de ejecuciones
   - Auditoría y debugging

2. **Reintentos automáticos**
   - Backoff exponencial
   - Dead letter queue
   - Alertas de fallos

3. **Monitoreo y métricas**
   - Endpoint de healthcheck
   - Prometheus metrics
   - Dashboard de estado

4. **Carga dinámica de plugins**
   - Servicios en archivo separado
   - Registry automático
   - Hot reload (seguro)

5. **Concurrencia**
   - Ejecutar servicios en paralelo
   - Locks distribuidos (si múltiples instancias)

---

**Última actualización:** 24 de marzo de 2026
