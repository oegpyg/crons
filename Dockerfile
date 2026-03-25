FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema para Pillow y compilación
RUN apt-get update && apt-get install -y \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la aplicación
COPY src/ .

# Ejecutar el scheduler principal
CMD ["python", "main.py"]
