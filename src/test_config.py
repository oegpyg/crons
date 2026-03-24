import os
import sys
import logging

# Agregar la ruta del proyecto
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.birthday import BirthdayService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_birthday_service():
    """Prueba cargar el servicio de cumpleaños."""
    print("\n🎂 Probando servicio de cumpleaños...")
    try:
        service = BirthdayService.from_env('BIRTHDAY_', os.environ.copy())
        
        if not service:
            logger.warning("⚠️  Servicio de cumpleaños está deshabilitado")
            return False
        
        logger.info(f"✅ Servicio cargado: {service.name}")
        logger.info(f"   Horario: {service.schedule}")
        logger.info(f"   Configuración: {len(service.config)} parámetros")
        
        return True
    except Exception as e:
        logger.error(f"❌ Error cargando servicio: {e}")
        return False


def test_db_connection():
    """Prueba la conexión a la BD."""
    print("\n📡 Probando conexión a MySQL...")
    try:
        service = BirthdayService.from_env('BIRTHDAY_', os.environ.copy())
        
        if not service:
            logger.warning("⚠️  Servicio no está habilitado, saltando prueba de BD")
            return True
        
        connection = service._get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            logger.info(f"✅ Conexión exitosa a MySQL - Versión: {version}")
        connection.close()
        return True
    except Exception as e:
        logger.error(f"❌ Error de conexión: {e}")
        return False


def test_query():
    """Prueba ejecutar el query de cumpleaños."""
    print("\n🎂 Probando query de cumpleaños...")
    try:
        service = BirthdayService.from_env('BIRTHDAY_', os.environ.copy())
        
        if not service:
            logger.warning("⚠️  Servicio no está habilitado")
            return True
        
        customers = service._get_birthday_customers()
        
        if customers:
            logger.info(f"✅ Query exitosa - {len(customers)} cliente(s) encontrado(s)")
            for customer in customers:
                logger.info(f"   - {customer['Name']} (Código: {customer['Code']})")
        else:
            logger.info("ℹ️  No hay cumpleaños hoy en la BD")
        
        return True
    except Exception as e:
        logger.error(f"❌ Error ejecutando query: {e}")
        return False


def test_notification():
    """Prueba enviar una notificación."""
    print("\n📤 Probando notificación...")
    
    try:
        service = BirthdayService.from_env('BIRTHDAY_', os.environ.copy())
        
        if not service:
            logger.warning("⚠️  Servicio no está habilitado")
            return True
        
        test_customer = {
            'Code': 'TEST001',
            'Name': 'Cliente Prueba',
            'Phone': '555-1234',
            'Mobile': '555-5678',
            'Address': 'Calle Test 123',
            'Cobrador': 'Probador',
            'dia': 24
        }
        
        result = service._send_notification(test_customer)
        
        if result:
            logger.info("✅ Notificación enviada exitosamente")
        else:
            logger.warning("⚠️  Notificación enviada pero puede haber problemas")
        
        return result
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False


def print_config():
    """Muestra la configuración cargada."""
    print("\n⚙️  Configuración de Servicios:")
    
    # Cumpleaños
    try:
        service = BirthdayService.from_env('BIRTHDAY_', os.environ.copy())
        if service:
            print(f"\n  ✅ Servicio: {service.name}")
            print(f"     Status: HABILITADO")
            print(f"     Horario: {service.schedule['hour']}:{str(service.schedule['minute']).zfill(2)}")
            print(f"     BD Host: {service.config.get('db_host', 'N/A')}")
            print(f"     Bot ID: {service.config.get('bot_id', 'N/A')}")
            print(f"     Chat ID: {service.config.get('chat_id', 'N/A')}")
        else:
            print(f"\n  ❌ Servicio: birthday_notifier")
            print(f"     Status: DESHABILITADO")
    except Exception as e:
        print(f"\n  ❌ Servicio: birthday_notifier")
        print(f"     Error: {e}")


def main():
    """Ejecuta todas las pruebas."""
    print("\n" + "="*60)
    print("🧪 PRUEBAS DEL SISTEMA MODULAR DE CRONS")
    print("="*60)
    
    print_config()
    
    tests = [
        ("Cargar Servicio", test_birthday_service),
        ("Conexión a MySQL", test_db_connection),
        ("Query de Cumpleaños", test_query),
        ("Notificación API", test_notification),
    ]
    
    results = {}
    for test_name, test_func in tests:
        results[test_name] = test_func()
    
    print("\n" + "="*60)
    print("📊 RESUMEN:")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ TODAS LAS PRUEBAS PASARON")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
