# Python 3.11 slim, suficiente para ML ligero en CPU
FROM python:3.11-slim

# Evitar prompts y optimizar pip
ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Dependencias del sistema (pandas, numpy, scikit-learn, jupyter, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    ca-certificates \
    tini \
 && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias Python
# PyTorch CPU desde index oficial, resto con pip
RUN python -m pip install --upgrade pip setuptools wheel \
 && python -m pip install --index-url https://download.pytorch.org/whl/cpu torch \
 && python -m pip install \
    scikit-learn \
    pandas \
    numpy \
    joblib \
    matplotlib \
    seaborn \
    jupyterlab \
    ipywidgets \
    python-dotenv \
    tqdm \
    tensorflow-cpu==2.16.1

# Crear estructura estándar (por si se build sin volúmenes)
RUN mkdir -p /app/src /app/data /app/models

# Usuario no-root (mejor práctica)
RUN useradd -ms /bin/bash appuser
USER appuser

# Exponer puerto de Jupyter
EXPOSE 8888

# tini como init
ENTRYPOINT ["/usr/bin/tini", "--"]

# Por defecto, no hace nada (usaremos docker compose para mandar comandos)
CMD ["bash", "-lc", "tail -f /dev/null"]
