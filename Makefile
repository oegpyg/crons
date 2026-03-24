.PHONY: help build up down logs restart test clean

help:
	@echo "🎂 Servicio de Notificaciones de Cumpleaños"
	@echo ""
	@echo "Comandos disponibles:"
	@echo "  make up          - Inicia el servicio"
	@echo "  make down        - Detiene el servicio"
	@echo "  make logs        - Muestra logs del servicio"
	@echo "  make restart     - Reinicia el servicio"
	@echo "  make test        - Ejecuta pruebas de configuración"
	@echo "  make build       - Construye la imagen Docker"
	@echo "  make clean       - Detiene y elimina todo"
	@echo "  make shell       - Abre shell en el contenedor"
	@echo "  make ps          - Muestra estado del servicio"

up:
	docker-compose up -d
	@echo "✅ Servicio iniciado"

down:
	docker-compose down
	@echo "✅ Servicio detenido"

logs:
	docker-compose logs -f push-notifier

restart:
	docker-compose restart birthday-notifier
	@echo "✅ Servicio reiniciado"

test:
	docker-compose exec push-notifier python test_config.py

build:
	docker-compose build
	@echo "✅ Imagen construida"

clean:
	docker-compose down
	@echo "✅ Servicio eliminado"

shell:
	docker-compose exec push-notifier /bin/bash

ps:
	docker-compose ps

check-logs-last:
	docker-compose logs --tail=50 push-notifier

env-setup:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Archivo .env creado (actualiza con tus valores)"; \
	else \
		echo "ℹ️  Archivo .env ya existe"; \
	fi
