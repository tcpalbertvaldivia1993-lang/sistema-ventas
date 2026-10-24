-- Título: Segmentación de clientes RFM
-- Pregunta: ¿Qué grupos de clientes tenemos según lo recientes, frecuentes y valiosos que son?
-- Técnicas: varias CTE encadenadas, julianday para diferencias de fechas, NTILE para puntuar de 1 a 4, CASE.
-- R = días desde la última compra, F = número de pedidos, M = importe total gastado.

WITH fecha_referencia AS (
    SELECT MAX(fecha) AS hoy FROM pedidos
),
rfm AS (
    SELECT
        cliente_id,
        julianday((SELECT hoy FROM fecha_referencia)) - julianday(MAX(fecha)) AS recencia_dias,
        COUNT(DISTINCT pedido_id)                                           AS frecuencia,
        SUM(importe_neto)                                                   AS monetario
    FROM v_ventas_detalle
    WHERE estado = 'completado'
    GROUP BY cliente_id
),
puntuaciones AS (
    SELECT
        *,
        NTILE(4) OVER (ORDER BY recencia_dias DESC) AS r,   -- 4 = compró hace poco
        NTILE(4) OVER (ORDER BY frecuencia)         AS f,   -- 4 = compra a menudo
        NTILE(4) OVER (ORDER BY monetario)          AS m    -- 4 = gasta mucho
    FROM rfm
),
segmentos AS (
    SELECT
        *,
        CASE
            WHEN r >= 4 AND f >= 4 THEN '1. Campeones'
            WHEN r >= 3 AND f >= 3 THEN '2. Leales'
            WHEN r >= 3            THEN '3. Recientes / potenciales'
            WHEN f >= 3            THEN '4. En riesgo'
            ELSE                        '5. Inactivos'
        END AS segmento_rfm
    FROM puntuaciones
)
SELECT
    segmento_rfm,
    COUNT(*)                                                    AS clientes,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)          AS pct_clientes,
    ROUND(SUM(monetario), 2)                                    AS ingresos,
    ROUND(100.0 * SUM(monetario) / SUM(SUM(monetario)) OVER (), 1) AS pct_ingresos,
    ROUND(AVG(recencia_dias), 0)                                AS recencia_media_dias,
    ROUND(AVG(frecuencia), 1)                                   AS pedidos_medios,
    ROUND(AVG(monetario), 2)                                    AS gasto_medio
FROM segmentos
GROUP BY segmento_rfm
ORDER BY segmento_rfm;
