# Makefile para el proyecto "introduccion"
# Simplifica comandos Docker y docker-compose

COMPOSE := docker-compose -f docker-compose.yml
SERVICE := introduccion-notebook

.PHONY: build up down restart logs shell notebook requirements

# Genera o actualiza requirements.txt basados en dependencias comunes de ML
requirements: ## Crea requirements.txt con las librerías del Colab
	echo "numpy" > requirements.txt
	echo "scipy" >> requirements.txt
	echo "matplotlib" >> requirements.txt
	echo "pandas" >> requirements.txt
	echo "scikit-learn" >> requirements.txt

build: down requirements ## Reconstruir red, dependencias y contenedores
	$(COMPOSE) up --build -d

up: ## Levantar contenedor en background
	$(COMPOSE) up -d

# Detiene y elimina contenedores y redes
down: ## Parar y eliminar contenedores y red
	$(COMPOSE) down

restart: down up ## Reiniciar contenedor

logs: ## Seguir logs del servicio
	$(COMPOSE) logs -f

shell: ## Acceder a una shell dentro del contenedor
	$(COMPOSE) exec $(SERVICE) bash

notebook: ## Mostrar URL del notebook
	@echo "Abre en tu navegador: http://localhost:8888/?token=$$JUPYTER_TOKEN"