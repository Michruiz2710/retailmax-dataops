"""Utilidades comunes: carga de configuracion por entorno y guardado de resultados."""

import os
from pathlib import Path

import pandas as pd
import yaml

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
ENTORNOS_VALIDOS = {"dev", "qa", "prod"}


def load_config(env: str | None = None) -> dict:
    """Carga config/<env>.yaml. El entorno se toma de APP_ENV si no se indica."""
    env = env or os.getenv("APP_ENV", "dev")
    if env not in ENTORNOS_VALIDOS:
        raise ValueError(f"Entorno no valido: {env}. Use uno de {ENTORNOS_VALIDOS}")
    with open(CONFIG_DIR / f"{env}.yaml", encoding="utf-8") as archivo:
        return yaml.safe_load(archivo)


def save_to_csv(df: pd.DataFrame, path: str) -> None:
    """Guarda un DataFrame en CSV creando la carpeta si no existe."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)