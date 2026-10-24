-- Título: Indicadores clave (KPIs)
-- Pregunta: ¿Cuál es la foto general del negocio en el periodo analizado?
-- Técnicas: agregaciones, subconsultas, CASE dentro de SUM.
-- Nota: los ingresos solo cuentan pedidos 'completado'.

SELECT
    MIN(p.fecha)                                                    AS desde,
    MAX(p.fecha)                                                    AS hasta,
    (SELECT ROUND(SUM(importe_neto), 2)
       FROM v_ventas_detalle WHERE estado = 'completado')           AS ingresos,
    (SELECT ROUND(100.0 * (SUM(importe_neto) - SUM(coste_total)) / SUM(importe_neto), 1)
       FROM v_ventas_detalle WHERE estado = 'completado')           AS margen_bruto_pct,
    SUM(CASE WHEN p.estado = 'completado' THEN 1 ELSE 0 END)        AS pedidos_completados,
    COUNT(DISTINCT CASE WHEN p.estado = 'completado' THEN p.cliente_id END) AS clientes_activos,
    (SELECT ROUND(SUM(importe_neto) / COUNT(DISTINCT pedido_id), 2)
       FROM v_ventas_detalle WHERE estado = 'completado')           AS ticket_medio,
    ROUND(100.0 * SUM(CASE WHEN p.estado <> 'completado' THEN 1 ELSE 0 END) / COUNT(*), 1)
                                                                    AS pct_cancelados_devueltos
FROM pedidos p;
