### SouthGermanCredit - Notebooks

Este directorio contiene dos cuadernos principales sobre el dataset South German Credit:

- P1_SouthGermanCredit.ipynb: regresión lineal desde cero (descenso por gradiente) con utilidades de diagnóstico y opcionalmente expansión polinómica de variables.
- P2_SouthGermanCredit.ipynb: clasificación (regresión logística desde cero) con split estratificado y preprocesamiento; incluye opción de polinomización.

Ambos notebooks incluyen detección robusta de la ruta del dataset y utilidades de visualización.

### Dataset

- Archivo: `introduccion/notebooks/data/SouthGermanCredit.asc`
- El código intenta resolver la ruta automáticamente desde varios directorios. Si no se encuentra, colócalo en `introduccion/notebooks/data/`.

### Requisitos

- Python 3.10+
- NumPy, Pandas, Matplotlib
- scikit-learn (opcional, requerido si habilitas interacciones polinómicas con `PolynomialFeatures`)

Instalación de dependencias sugerida:

```bash
pip install -r ../../requirements.txt
```

### P1_SouthGermanCredit.ipynb (Regresión)

- Flujo principal:
  - Carga y renombrado de columnas.
  - Split: 50% train, 25% val, 25% test (en el notebook base; puede variar).
  - Estandarización por columna (media y desvío de train).
  - Construcción de la matriz de diseño `x_inflated` con sesgo (columna de unos) en la primera columna.
  - Entrenamiento por descenso del gradiente con regularización opcional L1/L2.

- Expansión polinómica (configurable en la celda de `input`):
  - Variables de configuración dentro de la celda:
    - `POLY_COLUMNS`: lista de columnas a expandir (por nombre de `X_norm`).
    - `POLY_DEGREE`: grado máximo (entero ≥ 2).
    - `POLY_INTERACTIONS`: `False` para solo potencias por columna; `True` para incluir interacciones entre columnas listadas (requiere scikit-learn).
  - El pipeline reconstruye `input`, `x_inflated` y `feature_names` automáticamente al ejecutar la celda.

- Utilidades de gráficos:
  - `plot_regression_diagnostics(...)` muestra:
    - Serie real vs predicha contra el índice (con ordenamiento opcional `order`).
    - Dispersión real vs predicho con línea de identidad.
    - Residuales.
    - Historial de costo si pasas `cost_history`.
    - Barras de coeficientes (con o sin sesgo) ordenables por magnitud o valor.
  - Parámetros clave:
    - `x_axis`: permite graficar `y` contra una feature específica o un vector 1-D; si se pasa un índice de feature, el helper puede dibujar una curva de dependencia parcial manteniendo el resto de variables en su media.
    - `y_inv`: función para desnormalizar `y` (por ejemplo, volver de z-score a la escala original).
  - Gráfico de costo independiente:
    - `plot_cost_history(cost_history, title="...")`.

Ejemplos rápidos (dentro de P1):

```python
# Activar polinomización simple de 3 columnas, grado 3, sin interacciones
POLY_COLUMNS = ['credit_amount', 'duration_in_months', 'installment_rate']
POLY_DEGREE = 3
POLY_INTERACTIONS = False

# Tras ejecutar la celda de input, reentrena y grafica
cost_history_l2, theta_l2 = fit_model(x_inflated, output, theta, alpha=0.2, reg='l2', lam=0.1, steps=1500)
plot_cost_history(cost_history_l2, title='Costo - L2')
plot_regression_diagnostics(X=x_inflated, y_true=output, theta=theta_l2, feature_names=feature_names, title_prefix='L2', x_axis=1, partial_dependence=True)
```

```python
# Graficar y vs una variable base (array explícito), sin dependencia parcial
j = feature_cols.index('credit_amount')
plot_regression_diagnostics(
    X=x_inflated, y_true=output, theta=theta_l2,
    feature_names=feature_names, title_prefix='L2',
    x_axis=input[:, j], x_label='credit_amount', partial_dependence=False,
)
```

Notas:
- Si tu modelo es estrictamente lineal en las features, la dependencia parcial será una recta. Para curvas, necesitas no linealidades en la base (potencias y/o interacciones).

### P2_SouthGermanCredit.ipynb (Clasificación)

- Flujo principal (orientativo, puede variar según tu versión):
  - Split estratificado 60/20/20 sin scikit-learn, preservando proporciones de clases.
  - Estandarización por columna con protección a `std=0`.
  - Opción de polinomizar columnas (potencias y opcionalmente interacciones) para mejorar capacidad del modelo.
  - Implementación de regresión logística: inicialización de parámetros, función sigmoide, pérdida log-loss, actualización por descenso del gradiente.
  - Evaluación en val/test (métricas típicas: accuracy, AUC, etc. si están implementadas en tu versión).

Sugerencia para polinomización en P2:

```python
POLY_COLUMNS = feature_cols                      # o subset como ['credit_amount', 'duration_in_months']
POLY_DEGREE = 2                                  # ajusta según validación
POLY_INTERACTIONS = True                         # requiere scikit-learn o implementación propia
```

### Consejos de uso

- Ajusta `alpha` (tasa de aprendizaje), `lam` (regularización) y número de `steps` según convergencia; verifica el gráfico de costo para detectar divergencias.
- Cuando polinomices, considera re-escalar nuevamente las features expandidas para estabilizar el entrenamiento.
- Para interpretar coeficientes, usa `feature_names`; si agregas términos nuevos, asegúrate de extender los nombres.

### Estructura relacionada

- introduccion/notebooks/data/SouthGermanCredit.asc: dataset de entrada.
- introduccion/notebooks/P1_SouthGermanCredit.ipynb: notebook de regresión.
- introduccion/notebooks/P2_SouthGermanCredit.ipynb: notebook de clasificación.
- introduccion/notebooks/README.md: este documento.

### Problemas comunes

- Línea “recta” en gráficos: suele ser porque graficas contra el índice, o porque el modelo es lineal en las features. Usa `x_axis` con una variable y habilita no linealidades si esperas una curva.
- Costo no decrece: reduce `alpha`, reescala features expandidas o revisa `lam`.
- `ImportError` de scikit-learn: instala `scikit-learn` o desactiva interacciones (`POLY_INTERACTIONS=False`).


