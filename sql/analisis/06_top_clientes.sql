-- Título: Concentración de clientes (análisis de Pareto 80/20)
-- Pregunta: ¿Dependemos de pocos clientes? ¿Qué porcentaje de ingresos generan los mejores?
-- Técnicas: CTE, ROW_NUMBER, suma acumulada con SUM() OVER (ORDER BY ...), COUNT() OVER ().

WITH por_cliente AS (
    SELECT
        cliente_id,
        cliente,
        segmento,
        region,
        COUNT(DISTINCT pedido_id)  AS pedidos,
        SUM(importe_neto)          AS ingresos
    FROM v_ventas_detalle
    WHERE estado = 'completado'
    GROUP BY cliente_id, cliente, segmento, region
),
ranking AS (
    SELECT
        *,
        ROW_NUMBER() OVER (ORDER BY ingresos DESC)                         AS puesto,
        COUNT(*) OVER ()                                                   AS total_clientes,
        SUM(ingresos) OVER (ORDER BY ingresos DESC
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS ingresos_acumulados,
        SUM(ingresos) OVER ()                                              AS ingresos_totales
    FROM por_cliente
)
SELECT
    puesto,
    cliente,
    segmento,
    region,
    pedidos,
    ROUND(ingresos, 2)                                   AS ingresos,
    ROUND(100.0 * ingresos / ingresos_totales, 1)        AS pct_ingresos,
    ROUND(100.0 * ingresos_acumulados / ingresos_totales, 1) AS pct_acumulado,
    ROUND(100.0 * puesto / total_clientes, 1)            AS pct_clientes_acumulado
FROM ranking
ORDER BY puesto;
