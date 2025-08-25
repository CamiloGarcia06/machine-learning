# Usa una imagen oficial de Jupyter con SciPy y soporte para notebook
FROM jupyter/scipy-notebook:latest

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia código fuente y notebooks
COPY notebooks/ /app/notebooks/

# Copia el archivo de dependencias y las instala
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Exponer el puerto de Jupyter
EXPOSE 8888

# Arranca Jupyter Lab en el directorio de notebooks
CMD ["start-notebook.sh", "--NotebookApp.ip=0.0.0.0", "--NotebookApp.port=8888", "--NotebookApp.notebook_dir=/app/notebooks", "--NotebookApp.token=''"]