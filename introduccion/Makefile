# DO NOT CHANGE
MAIN_DIR := $(shell git rev-parse --show-toplevel)
DOCKER_DIR := $(MAIN_DIR)/introduccion
PROJECT_NAME ?= introduccion

# Definición de docker-compose sin file de entorno para evitar errores si no existe .env
COMPOSE := docker compose -f $(DOCKER_DIR)/docker-compose.yml --project-name $(PROJECT_NAME)
SERVICE := $(PROJECT_NAME)-notebook

.PHONY: help requirements build up down restart logs shell notebook rm

help: ## Muestra los comandos disponibles
	@grep -E '^[^[:space:]]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*## "} {printf "make %-12s # %s\n", $$1, $$2}'

requirements: ## Genera requirements.txt con librerías de ML
	@echo "Generando requirements.txt en $(DOCKER_DIR)..."
	echo "numpy" > $(DOCKER_DIR)/requirements.txt
	echo "scipy" >> $(DOCKER_DIR)/requirements.txt
	echo "matplotlib" >> $(DOCKER_DIR)/requirements.txt
	echo "pandas" >> $(DOCKER_DIR)/requirements.txt
	echo "scikit-learn" >> $(DOCKER_DIR)/requirements.txt

build: down requirements ## Reconstruir dependencias y contenedores
	$(COMPOSE) up --build -d

up: ## Levantar contenedores en background
	$(COMPOSE) up -d

down: ## Parar y eliminar contenedores y redes
down:
	$(COMPOSE) down -v --remove-orphans

restart: ## Reiniciar contenedores
	$(COMPOSE) restart

logs: ## Seguir logs del servicio
	$(COMPOSE) logs -f

shell: ## Abrir shell dentro del contenedor principal
	$(COMPOSE) exec $(SERVICE) bash

notebook: ## Mostrar URL de Jupyter
	@echo "Abre en navegador: http://localhost:8888"

rm: ## Eliminar contenedores, redes y limpiar imágenes
	@read -p "¿Eliminar todos los recursos Docker para $(PROJECT_NAME)? (y/n) " resp; \
	if [ "$$resp" = "y" ]; then \
		echo "Deteniendo y removiendo contenedores y redes..."; \
		$(COMPOSE) down -v --remove-orphans; \
		echo "Limpiando imágenes no usadas..."; \
		docker image prune -a -f; \
		echo "Operación completada."; \
	else \
		echo "Operación cancelada."; \
	fi