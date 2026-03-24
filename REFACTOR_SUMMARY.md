# ✨ Sistema Modular de Crons - Completo

¡Tu sistema de notificaciones está **totalmente refactorizado** a una arquitectura modular y escalable!

## 🎯 ¿Qué se hizo?

### Cambio Principal: De Monolítico a Modular

**ANTES:**
```
birthday_notifier.py → Ejecuta solo cumpleaños
            ↓
Para agregar otro servicio → Modificar código
```

**AHORA:**
```
CronManager (main.py)
    ├── BirthdayService (configuración independiente)
    ├── ServicioB (otro servicio, su propia config)
    └── ServicioC (fácil de agregar)

Todo desde .env, sin cambiar código
```

## 📁 Estructura Nueva

```
src/
├── main.py                    ← Scheduler principal
├── services/
│   ├── base_service.py       ← Clase base (abstract)
│   ├── birthday/
│   │   ├── __init__.py
│   │   └── service.py        ← Servicio de cumpleaños
│   └── (próximos servicios aquí)
└── test_config.py            ← Tests
```

## 🔑 Conceptos Clave

### 1. **BaseService**
Clase abstracta que todos los servicios heredan:
```python
class BaseService(ABC):
    name: str
    schedule: Dict
    enabled: bool
    
    @abstractmethod
    def execute(self) -> bool:
        pass
    
    @classmethod
    def from_env(env_prefix, env_vars):
        # Cargar desde .env automáticamente
        pass
```

### 2. **CronManager**
Gestor central que:
- Carga servicios desde `.env`
- Programa horarios automáticamente
- Ejecuta servicios de forma segura
- Maneja ciclo de vida completo

### 3. **Configuración por Servicio**
Cada servicio tiene su **prefijo** en `.env`:

```env
# Servicio 1
BIRTHDAY_ENABLED=true
BIRTHDAY_DB_HOST=...
BIRTHDAY_NOTIFICATIONS_API_URL=...

# Servicio 2 (cuando lo agregues)
OTRO_ENABLED=true
OTRO_PARAM1=...
OTRO_SCHEDULE_HOUR=9
```

## ⚡ Ventajas

✅ **Independencia**: Cada servicio funciona solo  
✅ **Extensibilidad**: Agregar servicios sin modificar existentes  
✅ **Configuración Descentralizada**: Todo en `.env`  
✅ **Sin Reinicio para Nuevos Servicios**: Agregar en `.env` y listo  
✅ **Testing Aislado**: Cada servicio se puede probar solo  
✅ **Escalable**: Soporta N servicios simultáneos  

## 🚀 Cómo Usar

### Iniciar el Sistema

```bash
# 1. Configurar
cp .env.example .env
nano .env          # Editar con tus valores

# 2. Iniciar
make up             # o: docker-compose up -d

# 3. Verificar
make logs           # Ver en tiempo real
make test           # Ejecutar pruebas
```

### Agregar un Nuevo Servicio

**3 pasos simple**:

1. **Crear servicio** (basado en [EXAMPLE_SERVICE.md](EXAMPLE_SERVICE.md))
2. **Registrar en main.py**:
   ```python
   service = MiServicio.from_env('MI_SERVICIO_', self.env_vars)
   if service:
       self.services.append(service)
   ```
3. **Configurar en .env**:
   ```env
   MI_SERVICIO_ENABLED=true
   MI_SERVICIO_PARAM1=valor1
   MI_SERVICIO_SCHEDULE_HOUR=9
   ```

**¡Eso es todo!** Reinicia y listo.

## 📚 Documentación

- **[README.md](README.md)** - Descripción general del proyecto
- **[QUICK_START.md](QUICK_START.md)** - Guía rápida de inicio
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Diseño detallado y extensibilidad
- **[EXAMPLE_SERVICE.md](EXAMPLE_SERVICE.md)** - Ejemplo de agregar nuevo servicio

## 🔧 Archivos Importantes

| Archivo | Propósito |
|---------|-----------|
| `src/main.py` | Scheduler principal - donde se cargan servicios |
| `src/services/base_service.py` | Clase base para todos los servicios |
| `src/services/birthday/service.py` | Implementación de Birthday Service |
| `.env.example` | Plantilla con todos los parámetros posibles |
| `docker-compose.yml` | Configuración del contenedor |

## 👨‍💼 Servicio Actual: Birthday Notifier

**Prefijo**: `BIRTHDAY_`

Parámetros:
- `ENABLED`: Habilitar/deshabilitar
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`: Conexión MySQL
- `NOTIFICATIONS_API_URL`: URL de la API
- `BOT_ID`, `CHAT_ID`: Identificadores de notificación
- `SCHEDULE_HOUR`, `SCHEDULE_MINUTE`: Horario ejecución

## 🎁 Bonus: Helpers

```bash
make up              # Iniciar
make down            # Detener
make logs            # Ver logs
make test            # Pruebas
make restart         # Reiniciar
make shell           # Bash en container
make ps              # Estado
```

## 🚦 Flujo de Ejecución

```
Docker Container Inicia
    ↓
main.py se ejecuta
    ↓
CronManager.start()
    ↓
    ├─ load_services()
    │  └─ Lee variables BIRTHDAY_, OTRO_, etc
    │     └─ Instancia servicios habilitados
    │
    ├─ schedule_services()
    │  └─ Programa cada servicio en su horario
    │
    └─ Scheduler comienza
       ├─ 6:00 AM → BirthdayService.run()
       ├─ 9:00 AM → OtroService.run() (si existe)
       └─ etc...
```

## 📊 Diferencias Antes/Después

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| Servicios | 1 (hardcoded) | N (dinámicos) |
| Agregar servicio | Modificar código | Configurar .env |
| Horarios | Hardcoded | Por servicio en .env |
| Parámetros | Variables globales | Por servicio en .env |
| Testing | Todo o nada | Independiente por servicio |
| Mantenimiento | Difícil con más servicios | Escalable |

## 🎓 Conceptos Aplicados

- **Polimorfismo**: BaseService define interfaz
- **Herencia**: Cada servicio hereda de BaseService
- **Inyección de Dependencias**: Config inyectada en constructor
- **Factory Pattern**: from_env() crea instancias
- **Single Responsibility**: Cada servicio hace una cosa
- **Open/Closed**: Abierto para extensión, cerrado para modificación

## ✅ Checklist de Uso

- [ ] Copié `.env.example` a `.env`
- [ ] Edité `.env` con mis valores reales
- [ ] Ejecuté `make up` para iniciar
- [ ] Ejecuté `make test` para verificar config
- [ ] Vi los logs en `make logs`
- [ ] Entendí la estructura en `ARCHITECTURE.md`
- [ ] Tengo lista la próxima idea de servicio

## 🎉 Listo

Tu sistema está **refactorizado, modular y listo para escalar**.

Prueba agregando un nuevo servicio usando [EXAMPLE_SERVICE.md](EXAMPLE_SERVICE.md).

---

**Última update**: 24 de marzo de 2026
