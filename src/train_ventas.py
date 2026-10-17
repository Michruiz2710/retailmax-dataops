"""Entrenamiento del modelo de prediccion de ventas de RetailMax.

Uso:  APP_ENV=dev python -m src.train_ventas
"""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from src.extract import extract_data
from src.transform import aggregate_sales, calculate_metrics, clean_data
from src.utils import load_config, save_to_csv

FEATURES = ["mes"]


def train_model(df: pd.DataFrame, model_path: str = "models/model.pkl"):
    """Entrena una regresion lineal (mes a venta_total) y la guarda con joblib."""
    X = df[FEATURES]
    y = df["venta_total"]
    modelo = LinearRegression().fit(X, y)
    r2 = r2_score(y, modelo.predict(X))
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo, model_path)
    return modelo, r2


def main() -> None:
    config = load_config()
    ventas = extract_data(config["database"]["path"])
    agregadas = aggregate_sales(calculate_metrics(clean_data(ventas)))
    save_to_csv(agregadas, config["outputs"]["aggregated_sales"])
    _, r2 = train_model(agregadas, config["outputs"]["model_path"])
    print(f"[{config['environment']}] Modelo entrenado. R2 = {r2:.3f}")


if __name__ == "__main__":
    main()