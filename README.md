# 🎂 Sistema Modular de Crons - Notificaciones

Sistema automatizado y extensible de servicios programados. Cada servicio es independiente, con su propia configuración y horario. Ideal para agregar nuevos servicios sin modificar el código existente.

## 📋 Características

- ✅ **Arquitectura Modular**: Cada servicio es independiente
- ✅ **Configuración por Servicio**: Cada uno con sus propios parámetros en `.env`
- ✅ **Fácil de Extender**: Agregar nuevos servicios es simple
- ✅ **BD Externa**: Se conecta a bases de datos configurables
- ✅ **Horarios Flexibles**: Cada servicio puede tener su propia hora de ejecución
- ✅ **Docker Ready**: Despliegue simple

## 🚀 Inicio Rápido

### Instalación

1. Preparar variables de entorno
```bash
cp .env.example .env
nano .env  # Editar con tus valores
```

2. Iniciar el servicio
```bash
docker-compose up -d
```

3. Verificar logs
```bash
docker-compose logs -f birthday-notifier
```

## 📁 Estructura del Proyecto

```
src/
├── main.py                     # Scheduler principal
├── services/
│   ├── base_service.py        # Clase base para servicios
│   └── birthday/
│       ├── __init__.py
│       └── service.py         # Servicio de cumpleaños
└── test_config.py             # Tests
```

## ⚙️ Configuración

Cada servicio se configura en la sección `.env` con su prefijo:

```env
# Servicio de cumpleaños
BIRTHDAY_ENABLED=true
BIRTHDAY_DB_HOST=tu-servidor-mysql.com
BIRTHDAY_DB_PORT=3306
BIRTHDAY_DB_USER=tu_usuario
BIRTHDAY_DB_PASSWORD=tu_password
BIRTHDAY_DB_NAME=netos_law
BIRTHDAY_NOTIFICATIONS_API_URL=http://tu-api:8888
BIRTHDAY_BOT_ID=1
BIRTHDAY_CHAT_ID=123456789
BIRTHDAY_SCHEDULE_HOUR=6
BIRTHDAY_SCHEDULE_MINUTE=0
```

## 🔧 Agregar un Nuevo Servicio

### 1. Crear la estructura
```bash
mkdir -p src/services/mi_servicio
touch src/services/mi_servicio/__init__.py
touch src/services/mi_servicio/service.py
```

### 2. Implementar el servicio

**src/services/mi_servicio/service.py:**
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
        # Validar parámetros requeridos
        required = ['param1', 'param2']
        missing = [k for k in required if k not in self.config]
        if missing:
            raise ValueError(f"Faltan: {missing}")
    
    def execute(self) -> bool:
        # Lógica del servicio
        self.logger.info("Ejecutando mi servicio...")
        return True
```

### 3. Registrar en main.py

En `src/main.py`, en el método `load_services()`:
```python
from services.mi_servicio import MiServicio

# ...

# Cargar nuevo servicio
service = MiServicio.from_env('MI_SERVICIO_', self.env_vars)
if service:
    self.services.append(service)
    logger.info(f"✅ Servicio cargado: {service.name}")
```

### 4. Configurar en .env

```env
MI_SERVICIO_ENABLED=true
MI_SERVICIO_PARAM1=valor1
MI_SERVICIO_PARAM2=valor2
MI_SERVICIO_SCHEDULE_HOUR=9
```

## 🧪 Pruebas

Ejecutar pruebas del sistema:
```bash
make test
```

Esto prueba:
- Carga de servicios
- Conexión a BD
- Queries
- API de notificaciones

## 📦 Servicios Disponibles

### 1. Birthday Notifier 🎂
**Prefijo**: `BIRTHDAY_`

Notifica cumpleaños de clientes consultando una BD MySQL.

**Parámetros**:
- `DB_HOST`: Servidor MySQL
- `DB_PORT`: Puerto (3306)
- `DB_USER`: Usuario
- `DB_PASSWORD`: Contraseña
- `DB_NAME`: Base de datos
- `NOTIFICATIONS_API_URL`: URL de API
- `BOT_ID`: ID del bot
- `CHAT_ID`: ID del chat
- `SCHEDULE_HOUR`: Hora ejecución (0-23)
- `SCHEDULE_MINUTE`: Minuto (0-59)

## 🎯 Flujo de Ejecución

```
1. main.py inicia
2. Carga todos los servicios desde .env
3. Programa cada servicio según su horario
4. Scheduler ejecuta servicios en su hora
5. Cada servicio:
   - Se conecta a sus BD configuradas
   - Ejecuta su lógica
   - Envía notificaciones
   - Registra en logs
```

## 🔍 Monitoreo

Ver logs en tiempo real:
```bash
docker-compose logs -f birthday-notifier
```

Ver estado:
```bash
docker-compose ps
```

Entrar al container:
```bash
docker-compose exec birthday-notifier bash
```

## 🐛 Solución de Problemas

### Servicio no se carga
```
Verificar:
- BIRTHDAY_ENABLED=true en .env
- Todos los parámetros requeridos presentes
- Ver logs para detalles del error
```

### Error de conexión BD
```
1. Verificar que BD es accesible:
   mysql -h DB_HOST -u DB_USER -p DB_NAME

2. Revisar credenciales en .env

3. Asegurar firewall permite conexión
```

### Notificación no se envía
```
1. Verificar NOTIFICATIONS_API_URL:
   curl http://api:8888/api/notifications/send

2. Verificar BOT_ID y CHAT_ID

3. Ver logs del container
```

## 📝 Arquitectura

### BaseService
Clase base que todos los servicios heredan. Define:
- Método `execute()` a implementar
- Método `from_env()` para cargar desde variables
- Manejo automático de errores y logging
- Interfaz estándar para el scheduler

### CronManager
Gestor central que:
- Carga servicios de forma dinámica
- Programa cada uno según su horario
- Ejecuta servicios de forma segura
- Maneja cycles de vida (start/shutdown)

## 📝 Logs

Todos los eventos se registran en los logs del contenedor:
- Verificaciones de cumpleaños
- Notificaciones enviadas/fallidas
- Errores de conexión

## 📦 Dependencias

- **PyMySQL**: Conexión a MySQL
- **requests**: HTTP requests a la API
- **APScheduler**: Programación de tareas cron
- **python-dotenv**: Manejo de variables de entorno

## 🔐 Seguridad

- No almacenes contraseñas en el código
- Usa `.env` para variables sensibles
- Mantén `.env` fuera del control de versiones (añadido a `.gitignore`)

## 📞 Soporte

Para reportar problemas o sugerencias, revisa los logs del container y verifica la configuración de variables de entorno.

---

**Última actualización**: 24 de marzo de 2026
