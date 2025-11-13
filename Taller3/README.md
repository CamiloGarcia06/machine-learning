# Cómo ejecutar el notebook del Taller 3 (local, Docker/Compose/Make o Colab)

Este README explica **cómo ejecutar el notebook existente** con todo el pipeline (limpieza, clustering, perfilado y análisis de consumo), **instalar dependencias** y una **breve guía de la estructura interna del notebook**.  
> No agrega contenidos nuevos: solo indica cómo **correr** lo que ya está.

---

## 📂 Supuestos mínimos del repo

- Un notebook principal, por ejemplo: `notebooks/Taller3.ipynb` *(si el nombre/ruta es otra, ajústalo en los comandos)*.
- El dataset **no se versiona**: debes tener `data/drug_consumption.data` (UCI ML).  
- Ya existen `Dockerfile` y `docker-compose.yml` en la raíz del proyecto. *(Solo los usamos)*
- (Opcional) `Makefile` con atajos (si ya lo tienes).

---

## ⚙️ Dependencias (si corres **local/venv**)
Python **3.10+** (recomendado 3.11) y:

```
numpy>=1.26
pandas>=2.1
scikit-learn>=1.4
scipy>=1.11
matplotlib>=3.8
joblib>=1.3
jupyterlab>=4.0
```

Instalación rápida (venv):
```bash
python -m venv .venv
# Activar
source .venv/bin/activate          # Linux/Mac
# .venv\Scripts\activate           # Windows PowerShell
# Instalar
pip install -U pip
pip install -r requirements.txt    # si existe
# o bien:
pip install numpy pandas scikit-learn scipy matplotlib joblib jupyterlab
```

---

## 🚀 Ejecución **local (venv)**

1) Coloca el dataset en `data/drug_consumption.data`.  
2) Lanza Jupyter:
```bash
jupyter lab
```
3) Abre `notebooks/Taller3.ipynb` y ejecuta todas las celdas (o por secciones).

> **Ruta del dataset**: el notebook incluye (o puedes usar) un snippet que busca `drug_consumption.data` en rutas típicas. Si falla, edita la variable `DATA_PATH` con la ruta absoluta.

---

## 🐳 Ejecución con **Docker / Docker Compose / Make**

### A) Docker (con Dockerfile existente)
Si tu `Makefile` ya define atajos, úsalos. Por ejemplo:
```bash
make d.build        # construye la imagen
make d.nb           # levanta Jupyter Lab (expone 8888 por defecto)
```
Luego abre `http://localhost:8888` y carga `notebooks/Taller3.ipynb`.

> Si no usas Make:  
> ```bash
> docker build -t taller3:latest .
> docker run --rm -p 8888:8888 -v "$PWD":/work -w /work taller3:latest \
>   jupyter lab --ip=0.0.0.0 --NotebookApp.token= --NotebookApp.password=
> ```

### B) Docker Compose (con `docker-compose.yml` existente)
Si tu Makefile lo envuelve:
```bash
make d.up      # docker compose up -d
make d.down    # docker compose down
```
O directamente:
```bash
docker compose up -d
# ... abre http://localhost:8888
docker compose down
```

> Asegúrate de que el volumen mapee el repo (para que el contenedor vea `notebooks/` y `data/`).

---

## 🧪 Ejecución en **Google Colab**

1) Abre Colab y sube el notebook `Taller3.ipynb` (o ábrelo desde Drive/GitHub).  
2) Instala dependencias mínimas:
```python
!pip -q install numpy pandas scikit-learn scipy matplotlib joblib
```
3) Sube el dataset o monta Drive:
```python
# Opción A: subir manualmente
from google.colab import files
_ = files.upload()  # selecciona drug_consumption.data

# Opción B: montar Drive
from google.colab import drive
drive.mount('/content/drive')
```
4) Ajusta la ruta del dataset (`DATA_PATH`) si no está en la misma carpeta del notebook (por ejemplo `/content/drug_consumption.data`).  
5) Ejecuta el notebook por completo o sección a sección.

---

## 🧭 Estructura del notebook (guía rápida)

El notebook está organizado (o se recomienda) en estos bloques:

1. **Setup & Carga de datos**  
   - Búsqueda robusta del archivo `drug_consumption.data`.  
   - Asignación de nombres de columna (32 columnas).  
2. **Limpieza**  
   - Normalización de etiquetas CL0–CL6 en las 19 drogas.  
   - Conversión de rasgos psicométricos y socio-demográficos a numéricos.  
   - Chequeos básicos de valores faltantes/outliers.
3. **Selección de features (X)**  
   - Solo variables **psicométricas y sociodemográficas** (edad, género, educación, país, etnia, N/E/O/A/C, Impulsiveness, SS).  
4. **Estandarización**  
   - `StandardScaler` sobre X.  
5. **PCA exploratoria** *(solo visualización)*  
   - Varianza explicada y dispersión PC1/PC2 coloreada por clúster.  
6. **Selección de K**  
   - K=2…10 con K-Means/Ward: **Elbow (inercia)**, **Silhouette**, **Calinski–Harabasz**, **Davies–Bouldin**.  
7. **Entrenamiento final**  
   - K elegido, `random_state=42`, `n_init=50` (K-Means).  
   - Guardado de **pipeline/labels/metadatos** en `final_artifacts/`.  
8. **Perfilado de clústeres**  
   - Medias/medianas/z-scores por feature y **heatmap**.  
   - **Silhouette plot** y **PCA 2D** coloreado por clúster.  
9. **Relación clúster ↔ consumo (19 drogas)**  
   - Binarización *ever/recent/frequent*.  
   - Prevalencias %, **χ²**, **V de Cramér**, BH-FDR.  
   - **Heatmap** y **barras apiladas**.  
10. **Sensibilidad y validación**  
   - Cambiar esquema de binarización y K alternativo; ARI/NMI/Jaccard/ρ.  
   - Detección de clústeres pequeños.
11. **Export de salidas**  
   - Tablas y figuras a carpetas: `eda_outputs/`, `profiling_outputs/`, `cluster_drug_relation_outputs/`, `sensitivity_outputs/`.

> Si algún bloque no aplica a tu versión del notebook, ignóralo; la idea es darte el mapa general.

---

## 🧰 Problemas comunes

- **FileNotFoundError** del dataset → verifica que `data/drug_consumption.data` exista o ajusta `DATA_PATH`.  
- **`Series.append` (pandas ≥2.0)** → usa `pd.concat` o construye dicts y crea `DataFrame`.  
- **Ward no tiene `.predict()`** → para inferencia, asigna al **centroide estandarizado más cercano**.  
- **K distintos entre particiones** → reporta **NMI/ARI** sin alinear; alinear solo para comparar descripciones por clúster base.

---

## 📤 Salidas principales
- `final_artifacts/` — pipeline(s) entrenados, labels y metadatos.  
- `profiling_outputs/` — z-scores/medias/medianas/figuras.  
- `cluster_drug_relation_outputs/` — prevalencias, χ², V de Cramér, BH.  
- `sensitivity_outputs/` — comparativas por esquema y K alternativo.

---
