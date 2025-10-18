# Taller 2 – Machine Learning

Repositorio de trabajo para el Taller 2 de la asignatura de Aprendizaje de Máquina. El proyecto incluye código Python, datos y recursos para entrenar y evaluar modelos clásicos y redes neuronales en CPU.

## Estructura

- `src/` código fuente y notebooks principales.
- `models/` artefactos entrenados (por ejemplo, normalizadores, pesos).
- `data/` dataset utilizados por los notebooks.
- `Dockerfile` imagen base con dependencias científicas y TensorFlow CPU.
- `docker-compose.yml` servicios para shell interactivo (`app`) y entorno Jupyter (`jupyter`).
- `Makefile` atajos para construir imágenes, ejecutar tests y limpiar artefactos.

## Requisitos locales

- Docker y Docker Compose instalados.
- Opcional: Python 3.11 si deseas ejecutar scripts sin contenedor (ver `requirements.txt`).

## Uso con Docker

```bash
# Construir imagen y levantar servicios con Makefile
make build
make up-jupyter

# Abrir un shell en el contenedor de desarrollo
docker compose run --rm app bash
```

Por defecto Jupyter se expone en `http://127.0.0.1:8888`. Si deseas protegerlo con token, exporta `JUPYTER_TOKEN=tu_token` antes de levantar el servicio.

### Atajos del Makefile

- `make build` compila la imagen definida en `Dockerfile`.
- `make up` levanta ambos servicios (`app` y `jupyter`) en segundo plano.
- `make up-app` o `make up-jupyter` levantan cada servicio por separado.
- `make shell` abre una sesión interactiva dentro del contenedor `app`.
- `make train` ejecuta `src/train.py` en el contenedor; `make predict` lanza `src/predict.py`.
- `make torch` comprueba rápidamente que PyTorch está instalado y detecta CUDA si aplica.
- `make down` apaga y limpia los contenedores; `make clean` borra artefactos como `answers.txt`.

## Ejecución local sin Docker

1. Crea un entorno virtual: `python -m venv .venv && source .venv/bin/activate`.
2. Instala dependencias: `pip install -r requirements.txt`.
3. Ejecuta los notebooks o scripts desde `src/`.

## Buenas prácticas

- Mantén los datos sensibles fuera del repositorio.
- Versiona únicamente modelos ligeros o necesarios para reproducibilidad.
- Usa los comandos del Makefile para tareas repetitivas (por ejemplo, `make format`, `make test` si están definidos).
