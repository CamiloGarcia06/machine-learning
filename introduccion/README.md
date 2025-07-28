# Proyecto: Introducción

Este repositorio contiene el trabajo **Introducción**, un entorno listo para experimentar con Jupyter Notebooks y Python para Machine Learning.

## Estructura del proyecto

```
machine_learning/
└─ introduccion/
   ├─ Dockerfile
   ├─ docker-compose.yml
   ├─ Makefile
   ├─ requirements.txt
   ├─ src/       # Código fuente (scripts y módulos)
   ├─ notebooks/ # Notebooks de Jupyter
   └─ README.md  # Documento de uso (este archivo)
```

## Prerrequisitos

* Docker
* Docker Compose
* Make

> Se asume que tienes Docker y Docker Compose instalados en tu máquina.

## Uso del Makefile

Todos los comandos se ejecutan desde la carpeta `introduccion`:

```bash
cd machine_learning/introduccion
```

### 1. Generar dependencias

Regenera el archivo `requirements.txt` con las librerías necesarias:

```bash
make requirements
```

### 2. Construir y levantar el contenedor

Construye la imagen Docker, instala dependencias y levanta el servicio en segundo plano:

```bash
make build
```

### 3. Levantar sin reconstruir

Si ya construiste la imagen y solo quieres iniciar el servicio:

```bash
make up
```

### 4. Detener y limpiar

Para detener y eliminar contenedores, redes y volúmenes asociados:

```bash
make down
```

### 5. Reiniciar

Ejecuta un `down` seguido de un `up`:

```bash
make restart
```

### 6. Ver logs

Sigue los registros en tiempo real:

```bash
make logs
```

### 7. Acceder al contenedor

Abre una shell dentro del contenedor:

```bash
make shell
```

### 8. URL del Notebook

Muestra la dirección para abrir Jupyter en tu navegador:

```bash
make notebook
# Por ejemplo: http://localhost:8888
```

> Si configuraste un token en `JUPYTER_TOKEN`, agrégalo como variable de entorno antes de `make build`:

```bash
export JUPYTER_TOKEN=mi_token_privado
make build
```
