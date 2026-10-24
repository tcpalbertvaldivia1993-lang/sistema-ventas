-- Título: Ventas por día de la semana
-- Pregunta: ¿Qué días de la semana concentran más pedidos?
-- Técnicas: strftime('%w') (0 = domingo), CASE para ordenar de lunes a domingo.

SELECT
    CASE strftime('%w', fecha)
        WHEN '1' THEN 'Lunes'   WHEN '2' THEN 'Martes'  WHEN '3' THEN 'Miércoles'
        WHEN '4' THEN 'Jueves'  WHEN '5' THEN 'Viernes' WHEN '6' THEN 'Sábado'
        ELSE 'Domingo'
    END                                                          AS dia,
    COUNT(DISTINCT pedido_id)                                    AS pedidos,
    ROUND(SUM(importe_neto), 2)                                  AS ingresos,
    ROUND(100.0 * COUNT(DISTINCT pedido_id)
          / SUM(COUNT(DISTINCT pedido_id)) OVER (), 1)           AS pct_pedidos
FROM v_ventas_detalle
WHERE estado = 'completado'
GROUP BY strftime('%w', fecha)
ORDER BY (CAST(strftime('%w', fecha) AS INTEGER) + 6) % 7;
