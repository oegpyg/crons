"""
Servicio de notificaciones de cumpleaños.
Hereda de BaseService para funcionar dentro del sistema modular.
"""

import logging
import requests
import pymysql
from typing import Dict, Any, List, Optional
from datetime import datetime
import os
import tempfile
import base64

from ..base_service import BaseService
from .image_generator import BirthdayImageGenerator

logger = logging.getLogger(__name__)


class BirthdayService(BaseService):
    """
    Servicio que notifica cumpleaños de clientes.
    
    Configuración requerida en .env (ejemplo con prefijo BIRTHDAY_):
        BIRTHDAY_ENABLED=true
        BIRTHDAY_DB_HOST=mysql.example.com
        BIRTHDAY_DB_PORT=3306
        BIRTHDAY_DB_USER=user
        BIRTHDAY_DB_PASSWORD=pass
        BIRTHDAY_DB_NAME=netos_law
        BIRTHDAY_NOTIFICATIONS_API_URL=http://api:8888
        BIRTHDAY_BOT_ID=1
        BIRTHDAY_CHAT_ID=123456789
        BIRTHDAY_SCHEDULE_HOUR=6
        BIRTHDAY_SCHEDULE_MINUTE=0
    """
    
    name = 'birthday_notifier'
    schedule = {
        'hour': 6,
        'minute': 0,
        'timezone': 'America/Asuncion'
    }
    
    def _validate_config(self):
        """Valida que la configuración tenga los campos requeridos."""
        required = [
            'db_host', 'db_port', 'db_user', 'db_password', 'db_name',
            'notifications_api_url', 'bot_id', 'chat_id'
        ]
        
        missing = [key for key in required if key not in self.config]
        if missing:
            raise ValueError(f"Configuración incompleta para {self.name}. Faltan: {missing}")
        
        # Leer schedule del config si está disponible
        if 'schedule_hour' in self.config:
            try:
                self.schedule['hour'] = int(self.config['schedule_hour'])
            except ValueError:
                pass
        
        if 'schedule_minute' in self.config:
            try:
                self.schedule['minute'] = int(self.config['schedule_minute'])
            except ValueError:
                pass
    
    def _get_db_connection(self) -> pymysql.Connection:
        """Crea conexión a la BD MySQL."""
        try:
            connection = pymysql.connect(
                host=self.config['db_host'],
                port=int(self.config['db_port']),
                user=self.config['db_user'],
                password=self.config['db_password'],
                database=self.config['db_name'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            return connection
        except Exception as e:
            self.logger.error(f"Error conectando a BD: {e}")
            raise
    
    def _get_birthday_customers(self) -> List[Dict[str, Any]]:
        """Obtiene clientes que cumplen años hoy."""
        connection = None
        try:
            connection = self._get_db_connection()
            with connection.cursor() as cursor:
                query = """
                    SELECT 
                        a.Code, 
                        a.Name, 
                        day(a.BirthDate) as dia, 
                        u.Name as Cobrador, 
                        a.Address, 
                        a.Phone, 
                        a.Mobile, 
                        a.BirthDate
                    FROM netos_law.Customer a
                    LEFT OUTER JOIN netos_law.User u ON u.Code=a.Collector
                    WHERE month(a.BirthDate) = month(now()) 
                        AND day(a.BirthDate) = day(now()) 
                        AND ifnull(a.Closed, 0) = 0 
                    ORDER BY day(a.BirthDate)
                """
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"Error ejecutando query: {e}")
            return []
        finally:
            if connection:
                connection.close()
    
    def _format_birthdate_spanish(self, birth_date) -> str:
        """Formatea la fecha de cumpleaños en español."""
        meses_es = {
            1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
            5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
            9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
        }
        
        if not birth_date:
            return 'N/A'
        
        try:
            if hasattr(birth_date, 'day'):
                dia = birth_date.day
                mes = meses_es.get(birth_date.month, 'N/A')
                anio = birth_date.year
                return f"{dia} de {mes} de {anio}"
            else:
                return str(birth_date)
        except Exception as e:
            self.logger.error(f"Error formateando fecha: {e}")
            return 'N/A'
    
    def _generate_and_send_images(self, customers: List[Dict[str, Any]]) -> bool:
        """Genera y envía imágenes de cumpleaños para cada cliente."""
        try:
            assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
            generator = BirthdayImageGenerator(assets_dir)
            
            images_sent = 0
            
            for customer in customers:
                try:
                    # Crear archivo temporal para la imagen
                    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
                        tmp_path = tmp_file.name
                    
                    # Generar imagen
                    if generator.generate_customer_image(customer, tmp_path):
                        # Leer imagen y convertir a base64
                        with open(tmp_path, 'rb') as img_file:
                            image_data = img_file.read()
                            image_base64 = base64.b64encode(image_data).decode('utf-8')
                            image_url = f"data:image/jpeg;base64,{image_base64}"
                        
                        # Preparar payload con imagen y texto
                        customer_name = customer.get('Name', 'Cliente')
                        message = f"🎂 ¡Feliz cumpleaños {customer_name}!"
                        
                        payload = {
                            "bot_id": int(self.config['bot_id']),
                            "chat_id": self.config['chat_id'],
                            "message": message,
                            "image_url": image_url,
                            "parse_mode": "HTML"
                        }
                        
                        # Enviar imagen
                        response = requests.post(
                            f"{self.config['notifications_api_url']}/api/notifications/send",
                            json=payload,
                            timeout=30  # Aumentar timeout por tamaño de base64
                        )
                        
                        if 200 <= response.status_code < 300:
                            images_sent += 1
                            self.logger.info(f"✅ Imagen enviada para {customer_name}")
                        else:
                            self.logger.warning(f"⚠️  Error enviando imagen de {customer_name}: {response.status_code}")
                    
                    # Limpiar archivo temporal
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
                        
                except Exception as e:
                    self.logger.error(f"Error procesando imagen de {customer.get('Name', 'Cliente')}: {e}")
                    continue
            
            if images_sent > 0:
                self.logger.info(f"✅ Se enviaron {images_sent}/{len(customers)} imágenes de cumpleaños")
            
            return images_sent > 0
            
        except Exception as e:
            self.logger.error(f"❌ Error generando imágenes: {e}")
            return False
    
    def _send_notification(self, customers: List[Dict[str, Any]]) -> bool:
        """Envía una notificación consolidada con todos los cumpleaños y genera imágenes personalizadas."""
        try:
            if not customers:
                return True
            
            # Construir mensaje con todos los cumpleaños
            message_lines = ["<b>🎂 ¡CUMPLEAÑOS DEL DÍA!</b>\n"]
            
            for customer in customers:
                birth_date = customer.get('BirthDate', '')
                formatted_date = self._format_birthdate_spanish(birth_date)
                cobrador = customer.get('Cobrador') or 'N/A'
                customer_mobile = customer.get('Mobile', '')
                customer_name = customer.get('Name', '')
                
                # Crear link de WhatsApp si tiene celular
                whatsapp_link = ""
                if customer_mobile:
                    # Limpiar número (solo dígitos)
                    clean_phone = ''.join(filter(str.isdigit, customer_mobile))
                    # Agregar código de país si no lo tiene (Paraguay = 595)
                    if not clean_phone.startswith('595'):
                        clean_phone = '595' + clean_phone
                    
                    message_wa = f"Feliz cumpleaños {customer_name}! 🎂"
                    # Encodificar el mensaje para URL
                    message_wa_encoded = requests.utils.quote(message_wa)
                    whatsapp_link = f'\n<a href="https://wa.me/{clean_phone}?text={message_wa_encoded}">📱 Enviar WhatsApp</a>'
                
                customer_info = f"""<b>{customer['Name']}</b>
<code>Código:</code> {customer['Code']}
<code>Fecha de Cumpleaños:</code> {formatted_date}
<code>Celular:</code> {customer['Mobile'] or 'N/A'}
<code>Cobrador:</code> {cobrador}{whatsapp_link}

"""
                message_lines.append(customer_info)
            
            message_lines.append(f"<b>Total: {len(customers)} cumpleaños</b>")
            
            message = "".join(message_lines)

            payload = {
                "bot_id": int(self.config['bot_id']),
                "chat_id": self.config['chat_id'],
                "message": message,
                "parse_mode": "HTML"
            }

            response = requests.post(
                f"{self.config['notifications_api_url']}/api/notifications/send",
                json=payload,
                timeout=10
            )

            text_sent = False
            if 200 <= response.status_code < 300:
                self.logger.info(f"✅ Notificación de texto enviada con {len(customers)} cumpleaños")
                text_sent = True
            else:
                self.logger.warning(f"⚠️  Error enviando notificación de texto: {response.status_code}")
            
            # Generar y enviar imágenes personalizadas (COMENTADO POR AHORA)
            # images_sent = self._generate_and_send_images(customers)
            
            # return text_sent or images_sent
            return text_sent
            
        except Exception as e:
            self.logger.error(f"❌ Error en notificación: {e}")
            return False
    
    def execute(self) -> bool:
        """Ejecuta la lógica del servicio de cumpleaños."""
        try:
            self.logger.info(f"Verificando cumpleaños...")
            
            customers = self._get_birthday_customers()
            
            if not customers:
                self.logger.info("No hay cumpleaños hoy")
                return True
            
            self.logger.info(f"Se encontraron {len(customers)} cumpleaños")
            
            # Enviar una sola notificación consolidada con todos los cumpleaños
            success = self._send_notification(customers)
            
            return success
        
        except Exception as e:
            self.logger.error(f"Error general: {e}", exc_info=True)
            return False
