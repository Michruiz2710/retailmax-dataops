"""Crea un snapshot fechado de la base de datos (estrategia de versionamiento)
Uso:  python -m scripts.create_snapshot data/ventas.db
Resultado: data/snapshots/ventas_AAAAMMDD.db
Se programa semanalmente con cron o con el DAG de Airflow
"""

import shutil
import sys
from datetime import date
from pathlib import Path


def create_snapshot(db_path: str, destino: str = "data/snapshots") -> Path:
    origen = Path(db_path)
    if not origen.exists():
        raise FileNotFoundError(f"No existe la base de datos: {db_path}")
    carpeta = Path(destino)
    carpeta.mkdir(parents=True, exist_ok=True)
    snapshot = carpeta / f"{origen.stem}_{date.today():%Y%m%d}{origen.suffix}"
    shutil.copy2(origen, snapshot)
    return snapshot


if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else "data/ventas.db"
    print(f"Snapshot creado: {create_snapshot(ruta)}")
