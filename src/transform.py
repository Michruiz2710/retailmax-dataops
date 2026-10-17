"""Limpieza, calculo de metricas y agregacion de ventas."""

import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina duplicados, rellena nulos y convierte la fecha a datetime."""
    limpio = df.drop_duplicates(subset=[c for c in df.columns if c != "id"]).copy()
    limpio["cantidad"] = limpio["cantidad"].fillna(0).astype(int)
    limpio["precio_unitario"] = limpio["precio_unitario"].fillna(
        limpio["precio_unitario"].mean()
    )
    limpio["fecha"] = pd.to_datetime(limpio["fecha"])
    return limpio.reset_index(drop=True)


def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega venta_total y mes."""
    resultado = df.copy()
    resultado["venta_total"] = resultado["cantidad"] * resultado["precio_unitario"]
    resultado["mes"] = resultado["fecha"].dt.month
    return resultado


def aggregate_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Suma venta_total por pais, categoria y mes."""
    return (
        df.groupby(["pais", "categoria", "mes"], as_index=False)["venta_total"]
        .sum()
        .sort_values(["pais", "categoria", "mes"])
        .reset_index(drop=True)
    )