"""Generación de datos ficticios de ventas.

Los datos son inventados pero incluyen patrones realistas a propósito
(estacionalidad, crecimiento, clientes muy valiosos, categorías con
márgenes distintos...) para que el análisis SQL tenga algo que descubrir.
Se usa una semilla fija, así que cada ejecución produce los mismos datos.
"""

import random
from datetime import date, timedelta

SEMILLA = 42
FECHA_INICIO = date(2024, 1, 1)
FECHA_FIN = date(2025, 12, 31)
NUM_CLIENTES = 300
NUM_PEDIDOS = 5000

REGIONES = ["Norte", "Sur", "Este", "Oeste", "Centro"]

# (nombre del vendedor, región, peso de asignación, tasa de cancelación/devolución)
VENDEDORES = [
    ("Laura Gómez", "Norte", 1.0, 0.07),
    ("Javier Ruiz", "Norte", 1.0, 0.07),
    ("Marta Sánchez", "Sur", 1.0, 0.07),
    ("Diego Torres", "Este", 1.0, 0.07),
    ("Lucía Navarro", "Este", 1.0, 0.07),
    ("Pablo Romero", "Oeste", 1.0, 0.07),
    ("Elena Castro", "Centro", 1.0, 0.07),
    ("Sergio Molina", "Centro", 0.45, 0.22),  # vendedor con bajo rendimiento
]

# Cada categoría: (margen aproximado, lista de productos (nombre, precio, popularidad))
# - Electrónica: mucho volumen y precio alto, pero margen bajo.
# - Accesorios: poco volumen, margen muy alto.
CATALOGO = {
    "Electrónica": (0.12, [
        ("Smartphone Pro X", 899.0, 3.0), ("Smartphone Lite", 349.0, 4.0),
        ("Televisor 55\"", 649.0, 2.5), ("Tablet 10\"", 299.0, 3.0),
        ("Auriculares inalámbricos", 129.0, 5.0), ("Smartwatch", 199.0, 3.0),
        ("Altavoz inteligente", 89.0, 3.5), ("Cámara deportiva", 249.0, 0.0),
    ]),
    "Informática": (0.22, [
        ("Portátil 14\"", 999.0, 2.0), ("Portátil gaming", 1499.0, 1.0),
        ("Monitor 27\"", 279.0, 2.5), ("Teclado mecánico", 89.0, 3.0),
        ("Ratón ergonómico", 39.0, 4.0), ("Disco SSD 1TB", 99.0, 3.0),
        ("Impresora multifunción", 159.0, 0.0),
    ]),
    "Hogar": (0.35, [
        ("Cafetera automática", 349.0, 1.5), ("Robot aspirador", 299.0, 2.0),
        ("Freidora de aire", 119.0, 3.5), ("Batidora de vaso", 69.0, 2.0),
        ("Lámpara LED", 35.0, 2.5), ("Juego de sartenes", 79.0, 2.0),
        ("Purificador de aire", 189.0, 0.8),
    ]),
    "Deportes": (0.40, [
        ("Bicicleta estática", 399.0, 0.8), ("Esterilla de yoga", 25.0, 3.0),
        ("Mancuernas 10kg", 49.0, 2.0), ("Zapatillas running", 109.0, 3.0),
        ("Mochila de senderismo", 69.0, 1.5), ("Pulsómetro", 79.0, 0.0),
    ]),
    "Moda": (0.50, [
        ("Chaqueta impermeable", 89.0, 2.0), ("Vaqueros clásicos", 49.0, 3.0),
        ("Camiseta básica", 15.0, 4.0), ("Zapatos de piel", 99.0, 1.5),
        ("Bufanda de lana", 29.0, 1.0), ("Gafas de sol", 59.0, 1.2),
    ]),
    "Accesorios": (0.65, [
        ("Funda de móvil", 19.0, 1.2), ("Cargador rápido", 29.0, 1.0),
        ("Cable USB-C", 12.0, 1.0), ("Soporte para portátil", 35.0, 0.6),
        ("Mochila para portátil", 55.0, 0.6), ("Protector de pantalla", 9.0, 0.8),
    ]),
}

NOMBRES = ["Ana", "Carlos", "María", "José", "Carmen", "David", "Isabel", "Antonio",
           "Laura", "Manuel", "Sofía", "Francisco", "Paula", "Daniel", "Raquel",
           "Alberto", "Cristina", "Miguel", "Beatriz", "Andrés", "Silvia", "Rubén"]
APELLIDOS = ["García", "Fernández", "González", "Rodríguez", "López", "Martínez",
             "Pérez", "Gómez", "Martín", "Jiménez", "Hernández", "Díaz", "Moreno",
             "Álvarez", "Muñoz", "Romero", "Alonso", "Gutiérrez", "Ortega", "Delgado"]
TIPOS_EMPRESA = ["Soluciones", "Distribuciones", "Comercial", "Servicios", "Grupo", "Talleres"]

# Factor estacional por mes: pico en Navidad y Black Friday, bajón en agosto
ESTACIONALIDAD = {1: 0.85, 2: 0.80, 3: 0.90, 4: 0.95, 5: 1.00, 6: 0.95,
                  7: 0.80, 8: 0.60, 9: 1.00, 10: 1.05, 11: 1.45, 12: 1.70}
# Factor por día de la semana (0 = lunes): más compras a final de semana
DIA_SEMANA = {0: 0.85, 1: 0.90, 2: 0.95, 3: 1.00, 4: 1.15, 5: 1.35, 6: 0.80}
CRECIMIENTO_ANUAL = 0.15


def _dias_del_periodo():
    """Devuelve todos los días del periodo y su peso relativo de ventas."""
    dias, pesos = [], []
    total_dias = (FECHA_FIN - FECHA_INICIO).days
    dia = FECHA_INICIO
    while dia <= FECHA_FIN:
        avance = (dia - FECHA_INICIO).days / total_dias  # de 0 a 1 a lo largo de los 2 años
        tendencia = 1 + CRECIMIENTO_ANUAL * 2 * avance
        dias.append(dia)
        pesos.append(tendencia * ESTACIONALIDAD[dia.month] * DIA_SEMANA[dia.weekday()])
        dia += timedelta(days=1)
    return dias, pesos


def _fecha_aleatoria(rng, desde, hasta):
    return desde + timedelta(days=rng.randint(0, (hasta - desde).days))


def generar_datos():
    """Genera todas las tablas como listas de tuplas listas para insertar."""
    rng = random.Random(SEMILLA)

    regiones = [(i, nombre) for i, nombre in enumerate(REGIONES, start=1)]
    id_region = {nombre: i for i, nombre in regiones}

    # --- Categorías y productos ---
    categorias, productos, popularidad = [], [], {}
    id_producto = 1
    for id_cat, (categoria, (margen, lista)) in enumerate(CATALOGO.items(), start=1):
        categorias.append((id_cat, categoria))
        for nombre, precio, popular in lista:
            margen_producto = max(0.05, margen + rng.uniform(-0.04, 0.04))
            coste = round(precio * (1 - margen_producto), 2)
            productos.append((id_producto, nombre, id_cat, precio, coste))
            popularidad[id_producto] = popular  # popularidad 0 = nunca se vende
            id_producto += 1

    # --- Vendedores ---
    vendedores, vendedores_por_region, info_vendedor = [], {}, {}
    for id_vend, (nombre, region, peso, tasa_fallo) in enumerate(VENDEDORES, start=1):
        vendedores.append((id_vend, nombre, id_region[region]))
        vendedores_por_region.setdefault(id_region[region], []).append(id_vend)
        info_vendedor[id_vend] = (peso, tasa_fallo)

    # --- Clientes ---
    # Cada cliente recibe un "peso de compra" con distribución de Pareto:
    # unos pocos compran muchísimo y la mayoría compra poco.
    clientes, peso_cliente = [], {}
    for id_cli in range(1, NUM_CLIENTES + 1):
        es_empresa = rng.random() < 0.2
        if es_empresa:
            nombre = f"{rng.choice(TIPOS_EMPRESA)} {rng.choice(APELLIDOS)} S.L."
        else:
            nombre = f"{rng.choice(NOMBRES)} {rng.choice(APELLIDOS)} {rng.choice(APELLIDOS)}"
        region = rng.choices(list(id_region.values()), weights=[1.3, 1.0, 1.1, 0.7, 1.6])[0]
        # La mayoría de clientes ya existen al inicio; el resto se da de alta durante el periodo
        if rng.random() < 0.45:
            fecha_alta = _fecha_aleatoria(rng, date(2022, 1, 1), FECHA_INICIO - timedelta(days=1))
        else:
            fecha_alta = _fecha_aleatoria(rng, FECHA_INICIO, date(2025, 10, 31))
        segmento = "Empresa" if es_empresa else "Particular"
        clientes.append((id_cli, nombre, f"cliente{id_cli:03d}@ejemplo.com",
                         region, fecha_alta.isoformat(), segmento))
        # Se limita el peso máximo para que ningún cliente acapare casi todas las ventas
        peso_cliente[id_cli] = min(rng.paretovariate(1.3), 15) * (2.0 if es_empresa else 1.0)

    # --- Pedidos y detalle ---
    dias, pesos_dias = _dias_del_periodo()
    fechas_pedidos = sorted(rng.choices(dias, weights=pesos_dias, k=NUM_PEDIDOS))
    ids_productos_vendibles = [p for p, popular in popularidad.items() if popular > 0]
    pesos_productos = [popularidad[p] for p in ids_productos_vendibles]

    pedidos, detalle = [], []
    for id_ped, fecha in enumerate(fechas_pedidos, start=1):
        # Solo pueden comprar los clientes ya dados de alta en esa fecha
        candidatos = [c for c in clientes if c[4] <= fecha.isoformat()]
        cliente = rng.choices(candidatos, weights=[peso_cliente[c[0]] for c in candidatos])[0]
        id_cli, region_cli, segmento = cliente[0], cliente[3], cliente[5]

        opciones = vendedores_por_region[region_cli]
        id_vend = rng.choices(opciones, weights=[info_vendedor[v][0] for v in opciones])[0]

        tasa_fallo = info_vendedor[id_vend][1]
        azar = rng.random()
        if azar < tasa_fallo * 0.6:
            estado = "cancelado"
        elif azar < tasa_fallo:
            estado = "devuelto"
        else:
            estado = "completado"
        pedidos.append((id_ped, id_cli, id_vend, fecha.isoformat(), estado))

        num_lineas = rng.choices([1, 2, 3, 4], weights=[45, 30, 15, 10])[0]
        elegidos = set()
        while len(elegidos) < num_lineas:
            elegidos.add(rng.choices(ids_productos_vendibles, weights=pesos_productos)[0])
        for id_prod in sorted(elegidos):
            precio = productos[id_prod - 1][3]
            if fecha.year == 2025:
                precio = round(precio * 1.03, 2)  # subida de tarifas en 2025
            if segmento == "Empresa":
                cantidad = rng.randint(2, 10)
                descuento = rng.choice([0.05, 0.10, 0.10, 0.15, 0.20])
            else:
                cantidad = rng.choices([1, 2, 3], weights=[75, 20, 5])[0]
                descuento = rng.choices([0, 0.05, 0.10], weights=[80, 12, 8])[0]
            detalle.append((id_ped, id_prod, cantidad, precio, descuento))

    return {
        "regiones": regiones,
        "categorias": categorias,
        "productos": productos,
        "vendedores": vendedores,
        "clientes": clientes,
        "pedidos": pedidos,
        "detalle_pedidos": detalle,
    }
