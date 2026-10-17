"""Pruebas unitarias de las variables de festivos"""

import pandas as pd

from src.features import add_es_festivo


def test_marca_festivo_segun_el_pais():
    df = pd.DataFrame(
        {
            "fecha": pd.to_datetime(["2026-07-20", "2026-07-20", "2026-03-03"]),
            "pais": ["CO", "PE", "MX"],
        }
    )
    resultado = add_es_festivo(df)
    # 20 de julio es festivo en Colombia pero no en Peru
    assert resultado["es_festivo"].tolist() == [1, 0, 0]


def test_no_modifica_el_dataframe_original():
    df = pd.DataFrame({"fecha": pd.to_datetime(["2026-01-01"]), "pais": ["CL"]})
    add_es_festivo(df)
    assert "es_festivo" not in df.columns
