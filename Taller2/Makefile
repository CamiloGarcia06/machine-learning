# Nombre del servicio principal en docker-compose
SVC=app
JUP=jupyter

PYTRAIN=python src/train.py
PYPRED=python src/predict.py

# ===== Helpers =====

.PHONY: help
help:
	@echo "Targets disponibles:"
	@echo "  build        - Construye la imagen"
	@echo "  up           - Levanta servicios (app + jupyter)"
	@echo "  up-app       - Levanta solo el servicio app"
	@echo "  up-jupyter   - Levanta solo Jupyter Lab en :8888"
	@echo "  down         - Baja los servicios"
	@echo "  shell        - Entra a una shell en el contenedor app"
	@echo "  train        - Ejecuta src/train.py dentro del contenedor"
	@echo "  predict      - Ejecuta src/predict.py dentro del contenedor"
	@echo "  torch        - Verifica instalación de PyTorch"
	@echo "  clean        - Limpia artefactos locales (answers.txt)"

# ===== Docker Compose =====

.PHONY: build
build:
	docker compose build --no-cache

.PHONY: up
up:
	docker compose up -d
	@echo "Jupyter abierto en http://localhost:8888"

.PHONY: up-app
up-app:
	docker compose up -d $(SVC)

.PHONY: up-jupyter
up-jupyter:
	docker compose up -d $(JUP)
	@echo "Jupyter abierto en http://localhost:8888"

.PHONY: down
down:
	docker compose down

.PHONY: shell
shell:
	docker compose exec $(SVC) bash

# ===== ML Workflow =====

# Entrena y guarda:
# - models/model_state.pth  (o el nombre que uses)
# - models/preprocess.joblib
.PHONY: train
train:
	docker compose exec $(SVC) bash -lc "$(PYTRAIN)"

# Lee quiz.csv y genera answers.txt en el repo
.PHONY: predict
predict:
	docker compose exec $(SVC) bash -lc "$(PYPRED)"

# Comprobación rápida de torch
.PHONY: torch
torch:
	docker compose exec $(SVC) python -c "import torch;print('Torch OK | CUDA:', torch.cuda.is_available())"

# ===== Limpieza =====

.PHONY: clean
clean:
	rm -f answers.txt

.PHONY: notebook
notebook:
	@echo "http://localhost:8888"
