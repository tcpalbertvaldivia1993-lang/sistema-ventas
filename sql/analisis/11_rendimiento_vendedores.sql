-- Título: Rendimiento del equipo comercial
-- Pregunta: ¿Qué vendedores rinden por encima o por debajo de la media y cuántos pedidos pierden?
-- Técnicas: agregación sobre pedidos y sobre ventas en dos CTE, JOIN entre ellas, AVG() OVER () para comparar con la media.

WITH pedidos_vendedor AS (
    SELECT
        vendedor_id,
        COUNT(*)                                                     AS pedidos_totales,
        SUM(CASE WHEN estado <> 'completado' THEN 1 ELSE 0 END)      AS pedidos_fallidos
    FROM pedidos
    GROUP BY vendedor_id
),
ventas_vendedor AS (
    SELECT
        vendedor_id,
        SUM(importe_neto)          AS ingresos,
        COUNT(DISTINCT pedido_id)  AS pedidos_completados
    FROM v_ventas_detalle
    WHERE estado = 'completado'
    GROUP BY vendedor_id
)
SELECT
    v.nombre                                                       AS vendedor,
    r.nombre                                                       AS region,
    pv.pedidos_totales,
    ROUND(100.0 * pv.pedidos_fallidos / pv.pedidos_totales, 1)     AS cancelados_devueltos_pct,
    ROUND(vv.ingresos, 2)                                          AS ingresos,
    ROUND(vv.ingresos / vv.pedidos_completados, 2)                 AS ticket_medio,
    ROUND(100.0 * (vv.ingresos - AVG(vv.ingresos) OVER ()) / AVG(vv.ingresos) OVER (), 1) AS vs_media_pct
FROM vendedores v
JOIN regiones r          ON r.id = v.region_id
JOIN pedidos_vendedor pv ON pv.vendedor_id = v.id
JOIN ventas_vendedor vv  ON vv.vendedor_id = v.id
ORDER BY ingresos DESC;
