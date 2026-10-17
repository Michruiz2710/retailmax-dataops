"""Pruebas UNITARIASrapidas y sin infraestructura."""

import pandas as pd

from src.transform import aggregate_sales, calculate_metrics, clean_data


def _muestra():
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4],
            "fecha": ["2026-01-05", "2026-01-05", "2026-02-10", "2026-02-11"],
            "pais": ["CO", "CO", "PE", "PE"],
            "producto": ["Celular", "Celular", "Sofa", "Sofa"],
            "categoria": ["tecnologia", "tecnologia", "hogar", "hogar"],
            "cantidad": [2, 2, None, 1],
            "precio_unitario": [100.0, 100.0, 50.0, None],
            "cliente_id": [1001, 1001, 1002, 1003],
        }
    )


def test_clean_data_elimina_duplicados():
    assert len(clean_data(_muestra())) == 3


def test_clean_data_rellena_nulos():
    limpio = clean_data(_muestra())
    assert limpio["cantidad"].isna().sum() == 0
    assert limpio["precio_unitario"].isna().sum() == 0
    assert limpio.loc[limpio["producto"] == "Sofa", "cantidad"].tolist()[0] == 0


def test_clean_data_convierte_fecha():
    assert pd.api.types.is_datetime64_any_dtype(clean_data(_muestra())["fecha"])


def test_calculate_metrics_venta_total():
    metricas = calculate_metrics(clean_data(_muestra()))
    assert metricas.loc[0, "venta_total"] == 200.0
    assert metricas.loc[0, "mes"] == 1


def test_aggregate_sales_agrupa_por_pais_categoria_mes():
    agregado = aggregate_sales(calculate_metrics(clean_data(_muestra())))
    assert list(agregado.columns) == ["pais", "categoria", "mes", "venta_total"]
    assert len(agregado) == 2
