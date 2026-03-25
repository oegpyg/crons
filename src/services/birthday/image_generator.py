"""
Generador de imágenes de cumpleaños dinámicas.
Crea imágenes personalizadas con logo y datos del cliente.
"""

import logging
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Any
import os
from datetime import datetime

logger = logging.getLogger(__name__)


class BirthdayImageGenerator:
    """Genera imágenes de cumpleaños personalizadas."""
    
    def __init__(self, assets_dir: str):
        """
        Inicializa el generador.
        
        Args:
            assets_dir: Ruta a la carpeta con assets (logo y fondo)
        """
        self.assets_dir = assets_dir
        self.background_path = os.path.join(assets_dir, 'cumple.jpg')
        self.logo_path = os.path.join(assets_dir, 'LOGO-300x78.png')
        
        if not os.path.exists(self.background_path):
            raise FileNotFoundError(f"Fondo no encontrado: {self.background_path}")
        if not os.path.exists(self.logo_path):
            raise FileNotFoundError(f"Logo no encontrado: {self.logo_path}")
    
    def generate_customer_image(self, customer: Dict[str, Any], output_path: str) -> bool:
        """
        Genera una imagen de cumpleaños para un cliente.
        
        Args:
            customer: Diccionario con datos del cliente
            output_path: Ruta donde guardar la imagen generada
            
        Returns:
            True si se generó exitosamente, False si hubo error
        """
        try:
            # Abrir imagen de fondo
            base_image = Image.open(self.background_path).convert('RGB')
            width, height = base_image.size
            
            logger.info(f"Base image size: {width}x{height}")
            
            # Abrir y redimensionar logo
            logo = Image.open(self.logo_path).convert('RGBA')
            logo_width = int(width * 0.25)  # Logo ocupa 25% del ancho
            aspect_ratio = logo.size[1] / logo.size[0]
            logo_height = int(logo_width * aspect_ratio)
            logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
            
            # Pegar logo en la esquina superior derecha
            logo_x = width - logo_width - 20
            logo_y = 20
            base_image.paste(logo, (logo_x, logo_y), logo)
            
            # Preparar datos del cliente
            customer_name = customer.get('Name', 'Cliente').upper()
            birth_date = self._format_birthdate_spanish(customer.get('BirthDate'))
            cobrador = customer.get('Cobrador', 'N/A')
            phone = customer.get('Mobile', 'N/A')
            
            # Crear objeto para dibujar
            draw = ImageDraw.Draw(base_image)
            
            # Intentar cargar fuentes (fallback a la fuente por defecto si no existen)
            try:
                title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
                text_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
                small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
            except:
                # Fallback a fuente por defecto
                logger.warning("No se pudieron cargar fuentes personalizadas, usando fuente por defecto")
                title_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # Colores
            text_color = (255, 255, 255)  # Blanco
            shadow_color = (0, 0, 0)  # Negro para sombra
            
            # Posiciones
            margin = 40
            text_x = margin
            
            # Dibujar sombra del nombre (efecto drop shadow)
            base_y = height // 2 - 80
            draw.text((text_x + 2, base_y + 2), customer_name, font=title_font, fill=shadow_color)
            draw.text((text_x, base_y), customer_name, font=title_font, fill=text_color)
            
            # Datos adicionales
            info_lines = [
                f"📅 {birth_date}",
                f"📱 {phone}",
                f"👤 Cobrador: {cobrador}"
            ]
            
            info_y = base_y + 100
            for line in info_lines:
                # Sombra
                draw.text((text_x + 1, info_y + 1), line, font=text_font, fill=shadow_color)
                # Texto
                draw.text((text_x, info_y), line, font=text_font, fill=text_color)
                info_y += 50
            
            # Guardar imagen
            base_image.save(output_path, 'JPEG', quality=95)
            logger.info(f"✅ Imagen generada: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error generando imagen: {e}")
            return False
    
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
            logger.error(f"Error formateando fecha: {e}")
            return 'N/A'
