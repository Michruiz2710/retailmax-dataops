# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#
# Notebook EXPORTADO a .py (formato "percent" de jupytext).
# El .ipynb no se versiona: sus salidas pesan, ensucian los diffs y pueden
# contener datos sensibles. Para abrirlo como notebook:
#     jupytext --to notebook notebooks/exploracion_ventas.py

# markdown
# # Exploracion de ventas RetailMax
# Analisis exploratorio basico sobre la base simulada de DEV.

# %%
from src.extract import extract_data
from src.transform import calculate_metrics, clean_data

ventas = extract_data("data/ventas.db")
ventas.head()

# markdown
## Calidad: porcentaje de nulos por columna

# %%
(ventas.isna().mean() * 100).round(2)

# markdown
# ## Ventas totales por pais y categoria

# %%
limpias = calculate_metrics(clean_data(ventas))
limpias.pivot_table(
    index="pais", columns="categoria", values="venta_total", aggfunc="sum"
).round(0)
