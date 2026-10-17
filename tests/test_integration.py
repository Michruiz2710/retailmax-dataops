"""Prueba de INTEGRACION"""

from src.extract import extract_data
from src.train_ventas import train_model
from src.transform import aggregate_sales, calculate_metrics, clean_data


def test_pipeline_completo(db_path, tmp_path):
    agregado = aggregate_sales(calculate_metrics(clean_data(extract_data(db_path))))

    assert not agregado.empty
    assert {"pais", "categoria", "mes", "venta_total"} <= set(agregado.columns)

    modelo_path = tmp_path / "model.pkl"
    _, r2 = train_model(agregado, str(modelo_path))
    assert modelo_path.exists()
    assert r2 <= 1.0
