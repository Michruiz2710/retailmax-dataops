"""Extraccion de ventas desde la base transaccional (SQLite simula PostgreSQL)."""

import sqlite3
from pathlib import Path

import pandas as pd

TABLAS_PERMITIDAS = {"ventas", "clientes"}


def extract_data(db_path: str, table: str = "ventas") -> pd.DataFrame:
    """Lee una tabla completa y la devuelve como DataFrame."""
    if table not in TABLAS_PERMITIDAS:
        raise ValueError(f"Tabla no permitida: {table}")
    path = Path(db_path)
    if not path.exists():
        raise FileNotFoundError(f"No existe la base de datos: {db_path}")
    with sqlite3.connect(path) as conn:
        # La tabla ya se valido contra TABLAS_PERMITIDAS.
        query = f"SELECT * FROM {table}"  # nosec B608
        return pd.read_sql_query(query, conn)