"""Variables adicionales para el modelo de ventas de dias festivos por pais"""

import pandas as pd

# Festivos nacionales de 2026 (muestra simplificada para el ejemplo)
FESTIVOS_2026 = {
    "CO": ["2026-01-01", "2026-05-01", "2026-07-20", "2026-08-07", "2026-12-25"],
    "PE": ["2026-01-01", "2026-05-01", "2026-07-28", "2026-07-29", "2026-12-25"],
    "MX": ["2026-01-01", "2026-02-02", "2026-03-16", "2026-09-16", "2026-12-25"],
    "CL": ["2026-01-01", "2026-05-01", "2026-09-18", "2026-09-19", "2026-12-25"],
    "EC": ["2026-01-01", "2026-05-01", "2026-05-24", "2026-08-10", "2026-12-25"],
}


def add_es_festivo(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega la columna es_festivo (1 si la venta cayo en un festivo de su pais)."""
    resultado = df.copy()
    fechas = resultado["fecha"].dt.strftime("%Y-%m-%d")
    resultado["es_festivo"] = [
        int(fecha in FESTIVOS_2026.get(pais, []))
        for fecha, pais in zip(fechas, resultado["pais"])
    ]
    return resultado
