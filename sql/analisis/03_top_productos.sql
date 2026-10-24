-- Título: Productos más vendidos
-- Pregunta: ¿Qué productos generan más ingresos y qué peso tienen sobre el total?
-- Técnicas: RANK() como función de ventana, porcentaje sobre el total con SUM() OVER ().

WITH por_producto AS (
    SELECT
        producto,
        categoria,
        SUM(cantidad)       AS unidades,
        SUM(importe_neto)   AS ingresos,
        SUM(coste_total)    AS coste
    FROM v_ventas_detalle
    WHERE estado = 'completado'
    GROUP BY producto, categoria
)
SELECT
    RANK() OVER (ORDER BY ingresos DESC)                     AS puesto,
    producto,
    categoria,
    unidades,
    ROUND(ingresos, 2)                                       AS ingresos,
    ROUND(100.0 * ingresos / SUM(ingresos) OVER (), 1)       AS pct_ingresos,
    ROUND(100.0 * (ingresos - coste) / ingresos, 1)          AS margen_pct
FROM por_producto
ORDER BY puesto;
