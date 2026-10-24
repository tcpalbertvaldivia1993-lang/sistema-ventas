-- Título: Productos sin ventas
-- Pregunta: ¿Hay productos en catálogo que nunca se han vendido?
-- Técnicas: NOT EXISTS (anti-join) para encontrar filas sin correspondencia.

SELECT
    pr.nombre                                         AS producto,
    c.nombre                                          AS categoria,
    pr.precio,
    pr.coste,
    ROUND(100.0 * (pr.precio - pr.coste) / pr.precio, 1) AS margen_teorico_pct
FROM productos pr
JOIN categorias c ON c.id = pr.categoria_id
WHERE NOT EXISTS (
    SELECT 1
    FROM detalle_pedidos d
    JOIN pedidos p ON p.id = d.pedido_id
    WHERE d.producto_id = pr.id AND p.estado = 'completado'
)
ORDER BY categoria, producto;
