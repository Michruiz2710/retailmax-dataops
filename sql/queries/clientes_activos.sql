-- Clientes activos segun la definicion MAESTRA v1.0 (config/mdm_cliente.json):
-- al menos una compra pagada en los ultimos 90 dias.
-- Todas las areas usan esta misma consulta
SELECT
    pais,
    COUNT(DISTINCT cliente_id) AS clientes_activos
FROM ventas
WHERE fecha >= date('now', '-90 days')
  AND cantidad > 0
GROUP BY pais;