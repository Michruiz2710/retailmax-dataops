\# Procedencia de los datos 



No versionamos los datos en Git: versionamos \*\*de donde vienen y que se les hizo\*\*.

Con esta informacion y el hash del archivo `.dvc` cualquier modelo se puede recrear.



| Dataset | Fuente | Extraccion | Transformaciones | Hash DVC | Definicion MDM |

|---|---|---|---|---|---|

| `ventas\_2026.parquet` | ERP de los 5 paises (CO, PE, MX, CL, EC) + POS de tiendas | 2026-10-01, `sql/queries/ventas\_por\_pais.sql` | `src/transform.py`: sin duplicados, nulos rellenados, `venta\_total` y `mes` calculados | `3f8a1c9e...` | Cliente activo v1.0 |

| `data/ventas.db` (DEV) | Sintetico: `scripts/create\_db.py`, semilla 42 | Se regenera con un comando | Ninguna (contiene nulos y duplicados a proposito) | No aplica | No aplica |



\## Como recrear el modelo de una fecha pasada



```bash

git checkout v1.0.0      # codigo, configuracion y punteros de esa version

dvc pull                 # descarga exactamente los datos de esa version

python -m src.train\_ventas

```



Cada modelo registrado guarda ademas el commit de Git y el hash de los datos con que se entreno. Asi se evita repetir el incidente del modelo de ventas de hace 4 meses que no se pudo reproducir.

