-- Título: Rentabilidad por categoría
-- Pregunta: ¿Qué categorías venden más y cuáles dejan realmente más margen?
-- Técnicas: GROUP BY, cálculo de margen, porcentaje sobre el total con ventana.

SELECT
    categoria,
    SUM(cantidad)                                                 AS unidades,
    ROUND(SUM(importe_neto), 2)                                   AS ingresos,
    ROUND(SUM(importe_neto) - SUM(coste_total), 2)                AS beneficio_bruto,
    ROUND(100.0 * (SUM(importe_neto) - SUM(coste_total)) / SUM(importe_neto), 1) AS margen_pct,
    ROUND(100.0 * SUM(importe_neto) / SUM(SUM(importe_neto)) OVER (), 1)          AS pct_ingresos,
    ROUND(100.0 * (SUM(importe_neto) - SUM(coste_total))
          / SUM(SUM(importe_neto) - SUM(coste_total)) OVER (), 1)                 AS pct_beneficio,
    ROUND(100.0 * AVG(descuento), 1)                              AS descuento_medio_pct
FROM v_ventas_detalle
WHERE estado = 'completado'
GROUP BY categoria
ORDER BY ingresos DESC;
