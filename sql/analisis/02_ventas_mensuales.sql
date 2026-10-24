-- Título: Evolución mensual de las ventas
-- Pregunta: ¿Las ventas crecen? ¿Cómo evoluciona cada mes frente al anterior y frente al mismo mes del año pasado?
-- Técnicas: CTE, strftime para agrupar por mes, funciones de ventana LAG.

WITH ventas_mes AS (
    SELECT
        strftime('%Y-%m', fecha)   AS mes,
        COUNT(DISTINCT pedido_id)  AS pedidos,
        SUM(importe_neto)          AS ingresos
    FROM v_ventas_detalle
    WHERE estado = 'completado'
    GROUP BY mes
)
SELECT
    mes,
    pedidos,
    ROUND(ingresos, 2) AS ingresos,
    ROUND(100.0 * (ingresos - LAG(ingresos) OVER (ORDER BY mes))
          / LAG(ingresos) OVER (ORDER BY mes), 1)          AS var_mes_anterior_pct,
    ROUND(100.0 * (ingresos - LAG(ingresos, 12) OVER (ORDER BY mes))
          / LAG(ingresos, 12) OVER (ORDER BY mes), 1)      AS var_anual_pct
FROM ventas_mes
ORDER BY mes;
