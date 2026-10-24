-- Título: Estacionalidad por mes del año
-- Pregunta: ¿En qué meses se vende más y menos? ¿Cuánto se aleja cada mes de un mes medio?
-- Técnicas: strftime, tabla de nombres con VALUES, índice estacional (100 = mes medio) con AVG() OVER ().

WITH nombres_mes (num, nombre) AS (
    VALUES (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'),
           (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
),
por_mes AS (
    SELECT
        CAST(strftime('%m', fecha) AS INTEGER)                    AS num_mes,
        SUM(importe_neto) / COUNT(DISTINCT strftime('%Y', fecha)) AS ingresos_medios
    FROM v_ventas_detalle
    WHERE estado = 'completado'
    GROUP BY num_mes
)
SELECT
    n.nombre                                                       AS mes,
    ROUND(pm.ingresos_medios, 2)                                   AS ingresos_medios_por_anio,
    ROUND(100.0 * pm.ingresos_medios / AVG(pm.ingresos_medios) OVER (), 0) AS indice_estacional
FROM por_mes pm
JOIN nombres_mes n ON n.num = pm.num_mes
ORDER BY pm.num_mes;
