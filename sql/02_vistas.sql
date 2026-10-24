-- =============================================================
-- Vista de ventas detalladas: une todas las tablas y calcula los
-- importes de cada línea. Simplifica las consultas de análisis.
-- =============================================================

CREATE VIEW v_ventas_detalle AS
SELECT
    p.id                                              AS pedido_id,
    p.fecha                                           AS fecha,
    p.estado                                          AS estado,
    c.id                                              AS cliente_id,
    c.nombre                                          AS cliente,
    c.segmento                                        AS segmento,
    r.nombre                                          AS region,
    v.id                                              AS vendedor_id,
    v.nombre                                          AS vendedor,
    pr.id                                             AS producto_id,
    pr.nombre                                         AS producto,
    cat.nombre                                        AS categoria,
    d.cantidad                                        AS cantidad,
    d.precio_unitario                                 AS precio_unitario,
    d.descuento                                       AS descuento,
    d.cantidad * d.precio_unitario * (1 - d.descuento) AS importe_neto,
    d.cantidad * pr.coste                             AS coste_total
FROM detalle_pedidos d
JOIN pedidos    p   ON p.id   = d.pedido_id
JOIN clientes   c   ON c.id   = p.cliente_id
JOIN regiones   r   ON r.id   = c.region_id
JOIN vendedores v   ON v.id   = p.vendedor_id
JOIN productos  pr  ON pr.id  = d.producto_id
JOIN categorias cat ON cat.id = pr.categoria_id;
