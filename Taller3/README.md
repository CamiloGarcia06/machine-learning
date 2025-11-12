# Taller 3 — Clustering en variables psico+sociodemográficas (Drug Consumption UCI)

Este repo contiene el **pipeline completo** para clusterizar individuos usando **únicamente** variables
psicométricas y sociodemográficas y, sobre los clústeres resultantes, analizar **patrones de consumo**
para 19 sustancias (binarizado según *ever / recent / frequent*).

Funciona en **Google Colab**, **local** (venv) o con **Docker** usando atajos del **Makefile**.

> Dataset: `drug_consumption.data` (UCI ML). No se versiona; colócalo en la ruta indicada abajo.

---

## 🧭 Estructura sugerida del proyecto

```
.
├── notebooks/
│   ├── 00_setup.ipynb
│   ├── 01_eda.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_k_selection.ipynb
│   ├── 04_stability.ipynb
│   ├── 05_final_training.ipynb
│   ├── 06_cluster_profiling.ipynb
│   └── 07_cluster_vs_consumption.ipynb
├── data/
│   └── drug_consumption.data         # <-- coloca aquí el archivo (no versionado)
├── src/                              # (opcional) helpers .py si los separas del notebook
├── requirements.txt
├── Makefile
├── docker-compose.yml (opcional)
└── README.md
```

### Carpetas de salidas (se crean en ejecución)
- `eda_outputs/`
- `k_selection_outputs/`
- `final_artifacts/` (pipeline K-Means/Ward, labels, metadatos)
- `profiling_outputs/`
- `cluster_drug_relation_outputs/`
- `sensitivity_outputs/<timestamp>/`

---

## 📦 Dependencias

Python **3.10+** (recomendado 3.11). Paquetes clave:
- `numpy`, `pandas`, `scikit-learn`, `scipy`, `matplotlib`, `joblib`, `jupyterlab`

Archivo sugerido `requirements.txt`:
```
numpy>=1.26
pandas>=2.1
scikit-learn>=1.4
scipy>=1.11
matplotlib>=3.8
joblib>=1.3
jupyterlab>=4.0
```

---

## 🚀 Uso en **Google Colab**

1) **Abrir** `notebooks/00_setup.ipynb` en Colab o crear uno nuevo.
2) **Instalar** dependencias mínimas:
   ```python
   !pip -q install numpy pandas scikit-learn scipy matplotlib joblib
   ```
3) **Subir** el dataset o montar Drive:
   ```python
   # Opción A: subir manual
   from google.colab import files
   up = files.upload()  # selecciona drug_consumption.data

   # Opción B: usar Google Drive
   from google.colab import drive
   drive.mount('/content/drive')

   # Ruta a tu dataset
   DATA_PATH = "/content/drug_consumption.data"   # o en tu Drive
   ```
4) **Cargar datos** (snippet robusto de búsqueda):
   ```python
   from pathlib import Path
   import pandas as pd

   NAME = "drug_consumption.data"
   CANDIDATES = [Path.cwd()/NAME, Path("/content")/NAME, Path("data")/NAME, Path.home()/"Downloads"/NAME]

   found = next((p for p in CANDIDATES if p.is_file()), None)
   if not found:
       hits = list(Path.cwd().rglob(NAME))
       found = hits[0] if hits else None
   if not found:
       raise FileNotFoundError("Coloca el dataset junto al notebook o define DATA_PATH manualmente.")
   DATA_PATH = found

   COLS = ["id","age","gender","education","country","ethnicity",
           "Nscore","Escore","Oscore","Ascore","Cscore","impulsive","SS",
           "alcohol","amphet","amyl","benzos","caff","cannabis","choc","coke",
           "crack","ecstasy","heroin","ketamine","legalh","lsd","meth","mushrooms",
           "nicotine","semer","vsa"]
   df = pd.read_csv(DATA_PATH, header=None, names=COLS)
   df.head()
   ```
5) Continúa con los notebooks **01 → 07** (EDA, limpieza, selección de K, estabilidad, entrenamiento final,
   perfilado y relación clúster↔consumo).

---

## 💻 Uso **local** (venv)

```bash
# 1) crear entorno
python -m venv .venv
# 2) activar
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows
# 3) instalar deps
pip install -U pip
pip install -r requirements.txt
# 4) ejecutar jupyter lab
jupyter lab
```
Coloca `data/drug_consumption.data` y abre los notebooks en `notebooks/`.

---

## 🐳 Uso con **Docker** + **Makefile**

### Requisitos
- Docker / Docker Desktop
- (opcional) Docker Compose
- GNU Make

### Atajos del **Makefile** (sugeridos)
> Si ya tienes un Makefile, verifica que los targets coincidan; si no, puedes adoptar estos:

```makefile
# --- Config ---
IMG ?= taller3:latest
NB_PORT ?= 8888
CONTAINER ?= taller3-nb

# --- Docker build ---
d.build: ## Construye la imagen
\tdocker build -t $(IMG) -f Dockerfile .

# --- Jupyter (docker run) ---
d.nb: ## Lanza Jupyter Lab (token vacío) en el puerto NB_PORT
\tdocker run --name $(CONTAINER) --rm -p $(NB_PORT):8888 \
\t  -v $(PWD):/work -w /work $(IMG) \
\t  jupyter lab --ip=0.0.0.0 --NotebookApp.token='' --NotebookApp.password=''

d.exec: ## Abre una shell dentro del contenedor en ejecución
\tdocker exec -it $(CONTAINER) bash

d.stop: ## Detiene el contenedor de Jupyter
\t-@docker stop $(CONTAINER)

# --- Compose (opcional) ---
d.up: ## Levanta stack con docker-compose
\tdocker compose up -d

d.down: ## Baja el stack
\tdocker compose down

.PHONY: d.build d.nb d.exec d.stop d.up d.down
```

### Dockerfile mínimo (sugerido)
Si no tienes uno, un ejemplo básico:
```dockerfile
FROM python:3.11-slim

RUN pip install --no-cache-dir \
    numpy pandas scikit-learn scipy matplotlib joblib jupyterlab

WORKDIR /work
EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--NotebookApp.token=", "--NotebookApp.password="]
```

### Comandos útiles
```bash
make d.build        # construir imagen
make d.nb           # iniciar Jupyter en http://localhost:8888
make d.exec         # entrar al contenedor
make d.stop         # detener Jupyter (docker run)
make d.up           # (si usas docker-compose) levantar
make d.down         # (si usas docker-compose) bajar
```

> Coloca el dataset en `data/drug_consumption.data` o móntalo desde tu host. El volumen `-v $(PWD):/work` ya sincroniza el repo.

---

## 🔁 Flujo de trabajo (resumen rápido)

1. **Limpieza**: normaliza CL0–CL6, asegura tipos numéricos (N,E,O,A,C, Impulsiveness, SS, age, gender, education, country, ethnicity).  
2. **Estandarización**: `StandardScaler` sobre features psico+socio.  
3. **Selección de K**: K=2…10 con **K-Means** y **Ward** usando **elbow**, **silhouette**, **CH**, **DB**.  
4. **Estabilidad**: bootstrap y perturbación (ARI/NMI).  
5. **Entrenamiento final**: fija `random_state=42`, `n_init=50` (K-Means). Guarda **pipeline**, **labels** y **metadatos**.  
6. **Perfilado**: medias/medianas por clúster, **z-scores**, heatmap, PCA 2D, silhouette plot.  
7. **Relación consumo**: binarización (*ever/recent/frequent*), prevalencias por clúster, **χ²**, **V de Cramér**, BH-FDR, heatmap y barras apiladas.  
8. **Sensibilidad/validación**: cambia esquema, prueba **K alternativo**, detecta clústeres <3–5%.

Las salidas se guardan en las carpetas mencionadas arriba para facilitar el **informe final**.

---

## 🔒 Reproducibilidad

- Semillas: usa `random_state=42` y `n_init=50` en K-Means.  
- Serializa artefactos:  
  - `final_artifacts/kmeans_pipeline.joblib`, `labels_kmeans.csv`, `kmeans_meta.json`  
  - (Ward) `ward_scaler.joblib`, `ward_centroids_scaled.npy`, `labels_ward.csv`, `ward_meta.json`  
- Incluye versiones en los metadatos (`numpy/pandas/sklearn`).

---

## 🧰 Troubleshooting

- **FileNotFoundError (dataset)**: verifica ruta `data/drug_consumption.data` o define `DATA_PATH` manualmente.  
- **Pandas ≥2.0**: `Series.append` fue eliminado → usa `pd.concat` o construye dicts/Series y `DataFrame`.  
- **Ward sin `.predict()`**: asigna por **centroide más cercano** en espacio estandarizado.  
- **K distintos** al comparar particiones: reporta **NMI/ARI** sin alinear; alinear solo para descripciones por clúster base.

---

## 📑 Licencia y cita de datos
El dataset proviene de UCI Machine Learning Repository. Consulta y respeta su licencia/cita oficial.
Este repo es solo con fines académicos.

---

¡Listo! Si quieres, puedo adaptar este README a la estructura exacta de tu repo (nombres de carpeta, servicios del `docker-compose`, etc.).
