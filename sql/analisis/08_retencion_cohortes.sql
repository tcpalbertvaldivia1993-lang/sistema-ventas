-- Título: Retención de clientes nuevos por cohorte
-- Pregunta: De los clientes que compran por primera vez cada trimestre, ¿cuántos vuelven a comprar?
-- Técnicas: CTE, cohortes por trimestre, EXISTS correlacionado, date() con modificadores.
-- Solo se incluyen clientes dados de alta desde 2024 (los anteriores no tienen su primera compra en los datos).
-- Si la ventana aún no ha terminado al final de los datos, el valor aparece vacío.

WITH compras AS (
    SELECT p.cliente_id, p.fecha
    FROM pedidos p
    JOIN clientes c ON c.id = p.cliente_id
    WHERE p.estado = 'completado' AND c.fecha_alta >= '2024-01-01'
),
primera_compra AS (
    SELECT
        cliente_id,
        MIN(fecha) AS fecha_primera,
        strftime('%Y', MIN(fecha)) || '-T' || ((CAST(strftime('%m', MIN(fecha)) AS INTEGER) + 2) / 3) AS cohorte
    FROM compras
    GROUP BY cliente_id
),
indicadores AS (
    SELECT
        pc.cohorte,
        pc.fecha_primera,
        EXISTS (SELECT 1 FROM compras x WHERE x.cliente_id = pc.cliente_id
                AND x.fecha > pc.fecha_primera AND x.fecha <= date(pc.fecha_primera, '+90 days'))  AS repite_90,
        EXISTS (SELECT 1 FROM compras x WHERE x.cliente_id = pc.cliente_id
                AND x.fecha > pc.fecha_primera AND x.fecha <= date(pc.fecha_primera, '+180 days')) AS repite_180,
        EXISTS (SELECT 1 FROM compras x WHERE x.cliente_id = pc.cliente_id
                AND x.fecha > pc.fecha_primera AND x.fecha <= date(pc.fecha_primera, '+365 days')) AS repite_365
    FROM primera_compra pc
),
limite AS (SELECT MAX(fecha) AS ultima FROM pedidos)
SELECT
    cohorte,
    COUNT(*) AS clientes_nuevos,
    CASE WHEN MAX(date(fecha_primera, '+90 days'))  <= (SELECT ultima FROM limite)
         THEN ROUND(100.0 * AVG(repite_90), 1)  END AS repiten_90d_pct,
    CASE WHEN MAX(date(fecha_primera, '+180 days')) <= (SELECT ultima FROM limite)
         THEN ROUND(100.0 * AVG(repite_180), 1) END AS repiten_180d_pct,
    CASE WHEN MAX(date(fecha_primera, '+365 days')) <= (SELECT ultima FROM limite)
         THEN ROUND(100.0 * AVG(repite_365), 1) END AS repiten_365d_pct
FROM indicadores
GROUP BY cohorte
ORDER BY cohorte;
