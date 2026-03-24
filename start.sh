#!/bin/bash

# Script para iniciar el entorno de desarrollo

echo "🚀 Iniciando Docker Compose..."
docker-compose up -d

echo "⏳ Esperando que MySQL esté listo..."
sleep 10

echo "📋 Mostrando logs del servicio..."
docker-compose logs -f birthday-notifier
