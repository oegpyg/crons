# 🚀 Guía Rápida - Sistema Modular de Crons

## Paso 1: Preparar Configuración

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar con tus valores (editor de tu preferencia)
nano .env
```

**Configurar valores para el servicio de cumpleaños:**

```env
BIRTHDAY_ENABLED=true

# Base de datos MySQL EXTERNA
BIRTHDAY_DB_HOST=tu-servidor-mysql.com
BIRTHDAY_DB_PORT=3306
BIRTHDAY_DB_USER=usuario
BIRTHDAY_DB_PASSWORD=contraseña
BIRTHDAY_DB_NAME=netos_law

# API de Notificaciones
BIRTHDAY_NOTIFICATIONS_API_URL=http://tu-api:8888
BIRTHDAY_BOT_ID=1
BIRTHDAY_CHAT_ID=123456789

# Horario (opcional, defecto 6:00 AM)
BIRTHDAY_SCHEDULE_HOUR=6
BIRTHDAY_SCHEDULE_MINUTE=0
```

## Paso 2: Inicia el Sistema

```bash
# Opción A: Con Docker Compose
docker-compose up -d

# Opción B: Con Make
make up
```

## Paso 3: Verifica la Configuración

```bash
# Ver logs en tiempo real
make logs

# O sin make:
docker-compose logs -f birthday-notifier
```

**Deberías ver algo como:**
```
✅ Servicio cargado: birthday_notifier
✅ Servicio 'birthday_notifier' programado: 6:00
🚀 Scheduler iniciado correctamente
```

## Paso 4: Ejecutar Prueba Inicial

```bash
# Ejecutar tests de configuración
make test
```

Esto valida:
- ✅ Carga del servicio
- ✅ Conexión a BD
- ✅ Ejecución de queries
- ✅ Envío de notificaciones

## ✅ Listo

El sistema ahora:
- ✅ Carga el servicio de cumpleaños desde `.env`
- ✅ Se ejecutará **diariamente a la hora configurada**
- ✅ Consultará cumpleaños en tu BD MySQL
- ✅ Enviará notificaciones automáticamente

## 🔧 Cambiar Hora de Ejecución

Sin modificar código, desde `.env`:

```env
BIRTHDAY_SCHEDULE_HOUR=9       # Cambiar a 9 AM
BIRTHDAY_SCHEDULE_MINUTE=30    # Cambiar a 9:30 AM
```

Luego reinicia:
```bash
make restart
```

## 📦 Comandos Útiles

```bash
make up              # Iniciar
make down            # Detener
make logs            # Ver logs
make test            # Ejecutar pruebas
make restart         # Reiniciar
make shell           # Acceder al container
make ps              # Ver estado
```

## 🐛 Problemas Comunes

### El servicio no se carga
```bash
# Ver logs detallados
docker-compose logs birthday-notifier

# Verificar:
# 1. BIRTHDAY_ENABLED=true en .env
# 2. Todos los parámetros requeridos presentes
```

### No conecta a BD MySQL
```bash
# Probar conexión manual
mysql -h BIRTHDAY_DB_HOST -u BIRTHDAY_DB_USER -p BIRTHDAY_DB_NAME

# Si no conecta:
# 1. Verificar IP/hostname es correcto
# 2. Verificar puerto (usualmente 3306)
# 3. Verificar firewall permite conexión
```

### Notificación no se envía
```bash
# Probar manualmente
curl http://BIRTHDAY_NOTIFICATIONS_API_URL/api/notifications/send \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"bot_id": 1, "chat_id": "123456789", "message": "test"}'

# Si no funciona:
# 1. Verificar URL es correcta
# 2. Verificar API está corriendo
# 3. Verificar BOT_ID y CHAT_ID
```

## 📝 Próximos Pasos

### Agregar Otro Servicio

1. Crear nuevo servicio (ver [ARCHITECTURE.md](ARCHITECTURE.md))
2. Registrarlo en `src/main.py`
3. Configurar en `.env`

Ejemplo:
```env
# Nuevo servicio
OTRO_ENABLED=true
OTRO_CONFIG_PARAM=valor
OTRO_SCHEDULE_HOUR=10
```

## 🎉 Eso es todo

Tu sistema de crons modular está corriendo y **listo para agregar más servicios**.

---

**Tip**: Los servicios se cargan y programan automáticamente desde `.env`. No requiere cambios de código.

