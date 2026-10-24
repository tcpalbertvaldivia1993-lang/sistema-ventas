-- =============================================================
-- Esquema de la base de datos de ventas
-- Modelo normalizado: dimensiones (regiones, clientes, categorías,
-- productos, vendedores) y hechos (pedidos y su detalle).
-- =============================================================

PRAGMA foreign_keys = ON;

DROP VIEW  IF EXISTS v_ventas_detalle;
DROP TABLE IF EXISTS detalle_pedidos;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS vendedores;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS categorias;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS regiones;

CREATE TABLE regiones (
    id      INTEGER PRIMARY KEY,
    nombre  TEXT NOT NULL UNIQUE
);

CREATE TABLE clientes (
    id          INTEGER PRIMARY KEY,
    nombre      TEXT NOT NULL,
    email       TEXT NOT NULL UNIQUE,
    region_id   INTEGER NOT NULL REFERENCES regiones(id),
    fecha_alta  TEXT NOT NULL,                       -- formato ISO 'AAAA-MM-DD'
    segmento    TEXT NOT NULL CHECK (segmento IN ('Particular', 'Empresa'))
);

CREATE TABLE categorias (
    id      INTEGER PRIMARY KEY,
    nombre  TEXT NOT NULL UNIQUE
);

CREATE TABLE productos (
    id            INTEGER PRIMARY KEY,
    nombre        TEXT NOT NULL UNIQUE,
    categoria_id  INTEGER NOT NULL REFERENCES categorias(id),
    precio        REAL NOT NULL,
    coste         REAL NOT NULL,
    CHECK (coste >= 0 AND precio > coste)
);

CREATE TABLE vendedores (
    id         INTEGER PRIMARY KEY,
    nombre     TEXT NOT NULL,
    region_id  INTEGER NOT NULL REFERENCES regiones(id)
);

CREATE TABLE pedidos (
    id           INTEGER PRIMARY KEY,
    cliente_id   INTEGER NOT NULL REFERENCES clientes(id),
    vendedor_id  INTEGER NOT NULL REFERENCES vendedores(id),
    fecha        TEXT NOT NULL,                      -- formato ISO 'AAAA-MM-DD'
    estado       TEXT NOT NULL CHECK (estado IN ('completado', 'cancelado', 'devuelto'))
);

CREATE TABLE detalle_pedidos (
    pedido_id        INTEGER NOT NULL REFERENCES pedidos(id),
    producto_id      INTEGER NOT NULL REFERENCES productos(id),
    cantidad         INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario  REAL NOT NULL CHECK (precio_unitario > 0),
    descuento        REAL NOT NULL DEFAULT 0 CHECK (descuento BETWEEN 0 AND 0.5),
    PRIMARY KEY (pedido_id, producto_id)
);

-- Índices para acelerar los filtros y uniones más habituales
CREATE INDEX idx_pedidos_fecha       ON pedidos(fecha);
CREATE INDEX idx_pedidos_cliente     ON pedidos(cliente_id);
CREATE INDEX idx_pedidos_vendedor    ON pedidos(vendedor_id);
CREATE INDEX idx_detalle_producto    ON detalle_pedidos(producto_id);
