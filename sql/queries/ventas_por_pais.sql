-- Ventas totales por pais y mes (alimenta el dashboard ejecutivo)
SELECT
    pais,
    strftime('%Y-%m', fecha)          AS mes,
    SUM(cantidad * precio_unitario)   AS venta_total,
    COUNT(DISTINCT cliente_id)        AS clientes_unicos
FROM ventas
WHERE cantidad IS NOT NULL
  AND precio_unitario IS NOT NULL
GROUP BY pais, strftime('%Y-%m', fecha)
ORDER BY pais, mes;