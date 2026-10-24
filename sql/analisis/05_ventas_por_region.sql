-- Título: Ventas por región
-- Pregunta: ¿Qué regiones aportan más y cuánto vale de media un cliente en cada una?
-- Técnicas: LEFT JOIN desde la dimensión (para no perder regiones sin ventas), COUNT DISTINCT.

SELECT
    r.nombre                                             AS region,
    COUNT(DISTINCT c.id)                                 AS clientes_registrados,
    COUNT(DISTINCT v.cliente_id)                         AS clientes_compradores,
    COUNT(DISTINCT v.pedido_id)                          AS pedidos,
    ROUND(COALESCE(SUM(v.importe_neto), 0), 2)           AS ingresos,
    ROUND(SUM(v.importe_neto) / COUNT(DISTINCT v.pedido_id), 2)  AS ticket_medio,
    ROUND(SUM(v.importe_neto) / COUNT(DISTINCT v.cliente_id), 2) AS ingresos_por_cliente,
    ROUND(100.0 * SUM(v.importe_neto) / SUM(SUM(v.importe_neto)) OVER (), 1) AS pct_ingresos
FROM regiones r
LEFT JOIN clientes c         ON c.region_id = r.id
LEFT JOIN v_ventas_detalle v ON v.cliente_id = c.id AND v.estado = 'completado'
GROUP BY r.nombre
ORDER BY ingresos DESC;
