"""Pruebas de ESQUEMA y CALIDAD DE DATOS
Si alguna falla el pipeline de CI/CD se detiene y el modelo no se entrena
"""

from datetime import datetime

import pytest

from src.transform import clean_data
from src.utils import load_config

COLUMNAS_ESPERADAS = [
    "id",
    "fecha",
    "pais",
    "producto",
    "categoria",
    "cantidad",
    "precio_unitario",
    "cliente_id",
]
PAISES_VALIDOS = {"CO", "PE", "MX", "CL", "EC"}
UMBRAL_NULOS = load_config("dev")["quality"]["max_null_pct"]


def test_esquema_columnas_esperadas(ventas):
    assert list(ventas.columns) == COLUMNAS_ESPERADAS


@pytest.mark.parametrize("columna", ["cantidad", "precio_unitario"])
def test_nulos_por_debajo_del_umbral(ventas, columna):
    porcentaje = ventas[columna].isna().mean()
    assert porcentaje <= UMBRAL_NULOS, f"{columna}: {porcentaje:.1%} de nulos"


def test_cantidad_no_negativa(ventas):
    assert (ventas["cantidad"].dropna() >= 0).all()


def test_precio_unitario_mayor_que_cero(ventas):
    assert (ventas["precio_unitario"].dropna() > 0).all()


def test_sin_fechas_futuras(ventas):
    assert (clean_data(ventas)["fecha"] <= datetime.now()).all()


def test_paises_validos(ventas):
    assert set(ventas["pais"]).issubset(PAISES_VALIDOS)


def test_ids_unicos(ventas):
    assert ventas["id"].is_unique
