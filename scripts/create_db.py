"""Crea una base SQLite de ventas simulada para DEV y pruebas.

Incluye a proposito algunos nulos y duplicados para que las pruebas de
calidad tengan algo que detectar. Nunca usa datos reales de clientes.

Uso:  python -m scripts.create_db data/ventas.db
"""

import random
import sqlite3
import sys
from datetime import date, timedelta
from pathlib import Path

PAISES = ["CO", "PE", "MX", "CL", "EC"]
PRODUCTOS = {
    "tecnologia": ["Portatil", "Celular", "Audifonos"],
    "hogar": ["Licuadora", "Sofa", "Lampara"],
    "moda": ["Camisa", "Zapatos", "Chaqueta"],
}


def create_db(db_path: str, n_registros: int = 300, seed: int = 42) -> str:
    # Datos sinteticos
    rng = random.Random(seed)  # nosec B311
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute("DROP TABLE IF EXISTS ventas")
        conn.execute("""CREATE TABLE ventas (
                id INTEGER PRIMARY KEY,
                fecha TEXT NOT NULL,
                pais TEXT NOT NULL,
                producto TEXT NOT NULL,
                categoria TEXT NOT NULL,
                cantidad INTEGER,
                precio_unitario REAL,
                cliente_id INTEGER NOT NULL
            )""")
        filas = []
        inicio = date(2026, 1, 1)
        for i in range(1, n_registros + 1):
            categoria = rng.choice(list(PRODUCTOS))
            cantidad = rng.randint(1, 10)
            precio = round(rng.uniform(10, 1500), 2)
            if i % 37 == 0:  # algunos nulos intencionales (< 10 %)
                cantidad = None
            if i % 41 == 0:
                precio = None
            filas.append(
                (
                    i,
                    (inicio + timedelta(days=rng.randint(0, 240))).isoformat(),
                    rng.choice(PAISES),
                    rng.choice(PRODUCTOS[categoria]),
                    categoria,
                    cantidad,
                    precio,
                    rng.randint(1000, 1999),
                )
            )
        # algunos duplicados intencionales (misma venta registrada dos veces)
        duplicados = [(n_registros + k + 1, *filas[k][1:]) for k in range(5)]
        conn.executemany(
            "INSERT INTO ventas VALUES (?, ?, ?, ?, ?, ?, ?, ?)", filas + duplicados
        )
    return db_path


if __name__ == "__main__":
    destino = sys.argv[1] if len(sys.argv) > 1 else "data/ventas.db"
    print(f"Base creada en {create_db(destino)}")