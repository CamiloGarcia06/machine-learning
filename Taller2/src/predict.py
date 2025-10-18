#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
predict.py — Lee el modelo y los artefactos de preprocesamiento, predice sobre data/quiz.csv
y genera answers.txt (una etiqueta por línea, en orden).
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model


# -------------------- rutas --------------------
QUIZ_PATH  = Path("data/quiz.csv")
MODELS_DIR = Path("models")
MODEL_CANDIDATES = [
    MODELS_DIR / "mlp_best.keras",     # recomendado (guardado con ModelCheckpoint)
    MODELS_DIR / "keras_model.keras",  # alternativo
]


# -------------------- utilidades --------------------
def _load_best_model():
    model_path = next((p for p in MODEL_CANDIDATES if p.exists()), None)
    if model_path is None:
        raise FileNotFoundError(
            f"No se encontró un modelo Keras. Busqué: {', '.join(str(p) for p in MODEL_CANDIDATES)}"
        )
    model = load_model(model_path)
    return model, model_path


def _load_prepro():
    """
    Intenta cargar preprocesamiento desde:
      1) prepro.json (preferido): num_cols, clip_bounds, means, stds, input_dim, n_classes
      2) meta.json + normalizer.npz (compat): num_cols, input_dim, n_classes, mean/std (sin clip)
    Devuelve: (num_cols, clip_bounds, mean_vec, std_vec, input_dim, n_classes)
    """
    prepro_json = MODELS_DIR / "prepro.json"
    meta_json   = MODELS_DIR / "meta.json"
    norm_npz    = MODELS_DIR / "normalizer.npz"

    if prepro_json.exists():
        prepro = json.loads(prepro_json.read_text())
        num_cols    = prepro["num_cols"]
        clip_bounds = prepro.get("clip_bounds", None)
        # convertir dicts de medias/stds a vectores 1D en el orden de num_cols
        means = np.array([prepro["means"][c] for c in num_cols], dtype=np.float32).reshape(-1)
        stds  = np.array([prepro["stds"][c]  for c in num_cols], dtype=np.float32).reshape(-1)
        input_dim = int(prepro["input_dim"])
        n_classes = int(prepro["n_classes"])
        return num_cols, clip_bounds, means, stds, input_dim, n_classes

    # compat: meta.json + normalizer.npz
    if not (meta_json.exists() and norm_npz.exists()):
        raise FileNotFoundError(
            "No encontré prepro.json ni (meta.json + normalizer.npz). "
            "Necesito artefactos de preprocesamiento para alinear/normalizar."
        )

    meta = json.loads(meta_json.read_text())
    num_cols  = meta["num_cols"]
    input_dim = int(meta["input_dim"])
    n_classes = int(meta["n_classes"])

    norm = np.load(norm_npz, allow_pickle=True)
    mean_arr = np.asarray(norm["mean"]).reshape(-1).astype(np.float32)
    std_arr  = np.asarray(norm["std"]).reshape(-1).astype(np.float32)

    if mean_arr.size != len(num_cols) or std_arr.size != len(num_cols):
        raise ValueError(
            f"Dim mismatch normalizer: mean={mean_arr.shape}, std={std_arr.shape}, "
            f"num_cols={len(num_cols)}"
        )

    clip_bounds = None  # en este modo no hay clipping
    return num_cols, clip_bounds, mean_arr, std_arr, input_dim, n_classes


def _apply_clip_and_standardize(df: pd.DataFrame,
                                num_cols,
                                clip_bounds,
                                mean_vec: np.ndarray,
                                std_vec:  np.ndarray) -> np.ndarray:
    """
    Aplica clipping por columna (si clip_bounds != None) y estandariza con mean/std.
    Retorna matriz float32 con columnas en el orden de num_cols.
    """
    X = df[num_cols].copy()

    # Clipping (winsorizing) si hay límites
    if clip_bounds:
        for c in num_cols:
            bounds = clip_bounds.get(c, None)
            if bounds is None:
                continue
            lo, hi = bounds
            # tolerancias por si hay None/NaN
            if lo is None or (isinstance(lo, float) and np.isnan(lo)):
                lo = -np.inf
            if hi is None or (isinstance(hi, float) and np.isnan(hi)):
                hi = np.inf
            X[c] = X[c].clip(lower=lo, upper=hi)

    # Estandarización
    eps = 1e-8
    std_safe = np.where(np.abs(std_vec) < eps, 1.0, std_vec).astype(np.float32)
    mean_vec = mean_vec.astype(np.float32)

    X_mat = X.to_numpy(dtype=np.float32)
    X_mat = (X_mat - mean_vec) / std_safe
    return X_mat


# -------------------- main --------------------
def main():
    # 0) Chequear quiz.csv
    if not QUIZ_PATH.exists():
        raise FileNotFoundError(f"No encontré {QUIZ_PATH}")

    # 1) Cargar modelo
    model, model_path = _load_best_model()

    # 2) Cargar artefactos de preprocesamiento
    num_cols, clip_bounds, mean_vec, std_vec, input_dim, n_classes = _load_prepro()

    # 3) Leer quiz y alinear columnas
    quiz_df = pd.read_csv(QUIZ_PATH)

    missing = [c for c in num_cols if c not in quiz_df.columns]
    if missing:
        raise ValueError(f"Faltan columnas esperadas en quiz.csv: {missing}")

    # 4) Transformar (clip + estandarizar)
    Xq = _apply_clip_and_standardize(quiz_df, num_cols, clip_bounds, mean_vec, std_vec)

    # 5) Chequeo de dimensión
    if Xq.shape[1] != input_dim:
        raise ValueError(f"Dimensiones no coinciden: Xq={Xq.shape[1]} vs input_dim={input_dim}")

    # 6) Predecir
    probs = model.predict(Xq, verbose=0)
    preds = probs.argmax(axis=1).astype(int)

    # 7) Guardar answers.txt
    out_path = Path("answers.txt")
    with out_path.open("w") as f:
        for p in preds:
            f.write(f"{p}\n")

    print(f"answers.txt generado ({len(preds)} líneas). Modelo: {model_path.name}")


if __name__ == "__main__":
    main()
