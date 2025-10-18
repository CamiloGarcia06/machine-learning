# Imagen oficial del stack Jupyter con TensorFlow ya instalado (CPU)
FROM quay.io/jupyter/tensorflow-notebook:python-3.11

# Paquetes de sistema opcionales
USER root
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*
USER $NB_USER

WORKDIR /home/jovyan

# (Opcional) instala extras de tu requirements si los tienes
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    if [ -f /tmp/requirements.txt ]; then pip install --no-cache-dir -r /tmp/requirements.txt; fi

RUN mkdir -p /home/jovyan/notebooks
EXPOSE 8888

CMD ["start-notebook.sh", "--NotebookApp.ip=0.0.0.0", "--NotebookApp.port=8888", "--NotebookApp.notebook_dir=/home/jovyan/notebooks", "--NotebookApp.token=''"]
