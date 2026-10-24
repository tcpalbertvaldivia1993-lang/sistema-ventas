"""Generación del informe en Markdown a partir de los resultados SQL.

Cada conclusión se calcula con los datos devueltos por las consultas,
así que si cambian los datos, cambian también las conclusiones.
"""

from datetime import date

MAX_FILAS = 25


def euros(valor):
    """Formatea un número como importe en euros: 1234567.8 -> '1.234.568 €'."""
    return f"{valor:,.0f} €".replace(",", ".")


def tabla_markdown(columnas, filas, max_filas=MAX_FILAS):
    """Convierte columnas y filas en una tabla Markdown."""
    def celda(valor):
        if valor is None:
            return "–"
        if isinstance(valor, float):
            return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return str(valor)

    lineas = ["| " + " | ".join(columnas) + " |",
              "|" + "|".join("---" for _ in columnas) + "|"]
    for fila in filas[:max_filas]:
        lineas.append("| " + " | ".join(celda(v) for v in fila) + " |")
    if len(filas) > max_filas:
        lineas.append(f"\n*Se muestran {max_filas} de {len(filas)} filas.*")
    return "\n".join(lineas)


def _como_dicts(resultado):
    return [dict(zip(resultado["columnas"], fila)) for fila in resultado["filas"]]


# --- Conclusiones de cada análisis -------------------------------------------
# Cada función recibe las filas (como diccionarios) y devuelve una lista de frases.

def _kpis(filas):
    k = filas[0]
    return [
        f"Entre {k['desde']} y {k['hasta']} se facturaron **{euros(k['ingresos'])}** "
        f"en {k['pedidos_completados']} pedidos completados de {k['clientes_activos']} clientes.",
        f"El ticket medio es de **{euros(k['ticket_medio'])}** y el margen bruto global "
        f"del **{k['margen_bruto_pct']} %**.",
        f"El {k['pct_cancelados_devueltos']} % de los pedidos se cancela o se devuelve.",
    ]


def _mensual(filas):
    por_anio = {}
    for f in filas:
        por_anio[f["mes"][:4]] = por_anio.get(f["mes"][:4], 0) + f["ingresos"]
    anios = sorted(por_anio)
    frases = []
    if len(anios) >= 2:
        a, b = anios[-2], anios[-1]
        crecimiento = 100 * (por_anio[b] - por_anio[a]) / por_anio[a]
        frases.append(f"Las ventas pasaron de {euros(por_anio[a])} en {a} a {euros(por_anio[b])} "
                      f"en {b}: un crecimiento del **{crecimiento:.1f} %**.")
    mejor = max(filas, key=lambda f: f["ingresos"])
    peor = min(filas, key=lambda f: f["ingresos"])
    frases.append(f"El mejor mes fue {mejor['mes']} ({euros(mejor['ingresos'])}) "
                  f"y el peor {peor['mes']} ({euros(peor['ingresos'])}).")
    return frases


def _productos(filas):
    top5 = sum(f["pct_ingresos"] for f in filas[:5])
    bajo_margen = [f["producto"] for f in filas[:10] if f["margen_pct"] < 5]
    frases = [f"Los 5 productos principales concentran el **{top5:.1f} %** de los ingresos; "
              f"el líder es *{filas[0]['producto']}* ({filas[0]['pct_ingresos']} %)."]
    if bajo_margen:
        frases.append(f"Ojo: entre los 10 más vendidos hay productos con margen inferior al 5 %: "
                      f"{', '.join(bajo_margen)}.")
    return frases


def _categorias(filas):
    mayor = max(filas, key=lambda f: f["ingresos"])
    mas_rentable = max(filas, key=lambda f: f["margen_pct"])
    mas_beneficio = max(filas, key=lambda f: f["beneficio_bruto"])
    return [
        f"**{mayor['categoria']}** genera el {mayor['pct_ingresos']} % de los ingresos pero solo el "
        f"{mayor['pct_beneficio']} % del beneficio (margen del {mayor['margen_pct']} %).",
        f"La categoría que más beneficio aporta es **{mas_beneficio['categoria']}** "
        f"({euros(mas_beneficio['beneficio_bruto'])}).",
        f"**{mas_rentable['categoria']}** tiene el mayor margen ({mas_rentable['margen_pct']} %) "
        f"pero apenas representa el {mas_rentable['pct_ingresos']} % de las ventas: hay margen para crecer.",
    ]


def _regiones(filas):
    primera, ultima = filas[0], filas[-1]
    mejor_cliente = max(filas, key=lambda f: f["ingresos_por_cliente"])
    return [
        f"**{primera['region']}** lidera con el {primera['pct_ingresos']} % de los ingresos; "
        f"**{ultima['region']}** queda última con el {ultima['pct_ingresos']} %.",
        f"En **{mejor_cliente['region']}** cada cliente vale más de media "
        f"({euros(mejor_cliente['ingresos_por_cliente'])}).",
    ]


def _pareto(filas):
    # Primer cliente a partir del cual ya se ha cubierto el 20 % de la cartera
    corte = next(f for f in filas if f["pct_clientes_acumulado"] >= 20)
    top3 = filas[2]["pct_acumulado"]
    empresas = sum(1 for f in filas[:10] if f["segmento"] == "Empresa")
    return [
        f"El **20 % de los clientes genera el {corte['pct_acumulado']} %** de los ingresos.",
        f"Solo los 3 primeros clientes suponen el {top3} % de la facturación: "
        f"hay un riesgo de dependencia elevado.",
        f"{empresas} de los 10 mejores clientes son empresas.",
    ]


def _rfm(filas):
    seg = {f["segmento_rfm"][3:]: f for f in filas}
    frases = []
    if "Campeones" in seg:
        c = seg["Campeones"]
        frases.append(f"Los **Campeones** son el {c['pct_clientes']} % de los clientes y aportan el "
                      f"{c['pct_ingresos']} % de los ingresos.")
    if "En riesgo" in seg:
        r = seg["En riesgo"]
        frases.append(f"Hay **{r['clientes']} clientes en riesgo** (compraban a menudo pero llevan "
                      f"~{r['recencia_media_dias']:.0f} días sin hacerlo) que representan "
                      f"{euros(r['ingresos'])} de ingresos históricos.")
    if "Inactivos" in seg:
        frases.append(f"El {seg['Inactivos']['pct_clientes']} % de la cartera está inactiva.")
    return frases


def _cohortes(filas):
    con_90 = [f["repiten_90d_pct"] for f in filas if f["repiten_90d_pct"] is not None]
    con_180 = [f["repiten_180d_pct"] for f in filas if f["repiten_180d_pct"] is not None]
    frases = []
    if con_90:
        frases.append(f"De media, el **{sum(con_90) / len(con_90):.1f} %** de los clientes nuevos "
                      f"repite compra en los primeros 90 días.")
    if con_180:
        frases.append(f"A los 180 días la recompra sube al {sum(con_180) / len(con_180):.1f} %: "
                      f"la primera experiencia de compra funciona bien.")
    return frases


def _estacionalidad(filas):
    alto = max(filas, key=lambda f: f["indice_estacional"])
    bajo = min(filas, key=lambda f: f["indice_estacional"])
    return [
        f"**{alto['mes']}** vende un {alto['indice_estacional'] - 100:.0f} % más que un mes medio; "
        f"**{bajo['mes']}** un {100 - bajo['indice_estacional']:.0f} % menos.",
        "Noviembre y diciembre (Black Friday y Navidad) son la temporada clave.",
    ]


def _dias(filas):
    ordenados = sorted(filas, key=lambda f: f["pct_pedidos"], reverse=True)
    a, b = ordenados[0], ordenados[1]
    return [f"**{a['dia']}** y **{b['dia']}** concentran el {a['pct_pedidos'] + b['pct_pedidos']:.1f} % "
            f"de los pedidos; {ordenados[-1]['dia']} es el día más flojo."]


def _vendedores(filas):
    peor = min(filas, key=lambda f: f["vs_media_pct"])
    media_fallos = sum(f["cancelados_devueltos_pct"] for f in filas) / len(filas)
    return [
        f"**{filas[0]['vendedor']}** lidera el equipo ({filas[0]['vs_media_pct']:+.1f} % sobre la media).",
        f"**{peor['vendedor']}** factura un {abs(peor['vs_media_pct'])} % menos que la media y tiene un "
        f"{peor['cancelados_devueltos_pct']} % de pedidos cancelados o devueltos "
        f"(media del equipo: {media_fallos:.1f} %).",
    ]


def _sin_ventas(filas):
    if not filas:
        return ["Todos los productos del catálogo tienen ventas."]
    nombres = ", ".join(f["producto"] for f in filas)
    return [f"Hay **{len(filas)} productos que nunca se han vendido**: {nombres}. "
            f"Conviene revisarlos o retirarlos del catálogo."]


CONCLUSIONES = {
    "01_kpis_generales": _kpis,
    "02_ventas_mensuales": _mensual,
    "03_top_productos": _productos,
    "04_categorias_margen": _categorias,
    "05_ventas_por_region": _regiones,
    "06_top_clientes": _pareto,
    "07_segmentacion_rfm": _rfm,
    "08_retencion_cohortes": _cohortes,
    "09_estacionalidad_mensual": _estacionalidad,
    "10_dia_semana": _dias,
    "11_rendimiento_vendedores": _vendedores,
    "12_productos_sin_ventas": _sin_ventas,
}


def conclusiones(resultados):
    """Devuelve {nombre_analisis: [frases]} para todos los análisis conocidos."""
    return {nombre: CONCLUSIONES[nombre](_como_dicts(res))
            for nombre, res in resultados.items() if nombre in CONCLUSIONES}


def recomendaciones(resultados):
    """Recomendaciones de negocio que combinan varios análisis."""
    cat = _como_dicts(resultados["04_categorias_margen"])
    vend = _como_dicts(resultados["11_rendimiento_vendedores"])
    rfm = {f["segmento_rfm"][3:]: f for f in _como_dicts(resultados["07_segmentacion_rfm"])}
    mayor = max(cat, key=lambda f: f["ingresos"])
    rentable = max(cat, key=lambda f: f["margen_pct"])
    peor = min(vend, key=lambda f: f["vs_media_pct"])
    en_riesgo = rfm.get("En riesgo", {}).get("clientes", 0)
    return [
        f"**Revisar precios y descuentos en {mayor['categoria']}**: es la categoría que más factura "
        f"pero la que menos margen deja ({mayor['margen_pct']} %).",
        f"**Impulsar la venta cruzada de {rentable['categoria']}** (margen del {rentable['margen_pct']} %) "
        f"junto a los productos más vendidos.",
        f"**Lanzar una campaña de reactivación** para los {en_riesgo} clientes en riesgo antes de perderlos.",
        "**Crear un programa de cuentas clave** para los mejores clientes: unos pocos concentran gran parte "
        "de la facturación y su pérdida tendría un gran impacto.",
        "**Planificar stock, personal y campañas** para noviembre-diciembre y aprovechar la caída de "
        "julio-agosto para promociones.",
        f"**Analizar los pedidos fallidos de {peor['vendedor']}** y reforzar su formación o seguimiento.",
        "**Revisar los productos sin ventas** para liberar catálogo y stock inmovilizado.",
    ]


def generar_informe(resultados):
    """Construye el texto completo del informe en Markdown."""
    partes = [
        "# Informe de análisis de ventas",
        "",
        f"*Generado automáticamente el {date.today().isoformat()} a partir de la base de datos "
        "SQLite `ventas.db`. Los datos son ficticios.*",
        "",
        "## Índice",
        "",
    ]
    for i, res in enumerate(resultados.values(), start=1):
        partes.append(f"{i}. {res['titulo']}")
    partes.append(f"{len(resultados) + 1}. Recomendaciones para la empresa")
    partes.append("")

    textos = conclusiones(resultados)
    for i, (nombre, res) in enumerate(resultados.items(), start=1):
        partes += [
            f"## {i}. {res['titulo']}",
            "",
            f"**Pregunta de negocio:** {res['pregunta']}  ",
            f"**Consulta:** [`sql/analisis/{nombre}.sql`](../sql/analisis/{nombre}.sql)",
            "",
            tabla_markdown(res["columnas"], res["filas"]),
            "",
            "**Conclusiones:**",
            "",
        ]
        partes += [f"- {frase}" for frase in textos.get(nombre, [])]
        partes.append("")

    partes += [f"## {len(resultados) + 1}. Recomendaciones para la empresa", ""]
    partes += [f"{i}. {texto}" for i, texto in enumerate(recomendaciones(resultados), start=1)]
    partes.append("")
    return "\n".join(partes)
