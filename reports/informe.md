# Informe de análisis de ventas

*Generado automáticamente el 2026-10-24 a partir de la base de datos SQLite `ventas.db`. Los datos son ficticios.*

## Índice

1. Indicadores clave (KPIs)
2. Evolución mensual de las ventas
3. Productos más vendidos
4. Rentabilidad por categoría
5. Ventas por región
6. Concentración de clientes (análisis de Pareto 80/20)
7. Segmentación de clientes RFM
8. Retención de clientes nuevos por cohorte
9. Estacionalidad por mes del año
10. Ventas por día de la semana
11. Rendimiento del equipo comercial
12. Productos sin ventas
13. Recomendaciones para la empresa

## 1. Indicadores clave (KPIs)

**Pregunta de negocio:** ¿Cuál es la foto general del negocio en el periodo analizado?  
**Consulta:** [`sql/analisis/01_kpis_generales.sql`](../sql/analisis/01_kpis_generales.sql)

| desde | hasta | ingresos | margen_bruto_pct | pedidos_completados | clientes_activos | ticket_medio | pct_cancelados_devueltos |
|---|---|---|---|---|---|---|---|
| 2024-01-01 | 2025-12-31 | 4.386.583,39 | 14,50 | 4568 | 293 | 960,29 | 8,60 |

**Conclusiones:**

- Entre 2024-01-01 y 2025-12-31 se facturaron **4.386.583 €** en 4568 pedidos completados de 293 clientes.
- El ticket medio es de **960 €** y el margen bruto global del **14.5 %**.
- El 8.6 % de los pedidos se cancela o se devuelve.

## 2. Evolución mensual de las ventas

**Pregunta de negocio:** ¿Las ventas crecen? ¿Cómo evoluciona cada mes frente al anterior y frente al mismo mes del año pasado?  
**Consulta:** [`sql/analisis/02_ventas_mensuales.sql`](../sql/analisis/02_ventas_mensuales.sql)

| mes | pedidos | ingresos | var_mes_anterior_pct | var_anual_pct |
|---|---|---|---|---|
| 2024-01 | 139 | 120.960,80 | – | – |
| 2024-02 | 125 | 118.486,05 | -2,00 | – |
| 2024-03 | 150 | 152.978,30 | 29,10 | – |
| 2024-04 | 164 | 200.249,40 | 30,90 | – |
| 2024-05 | 171 | 146.046,40 | -27,10 | – |
| 2024-06 | 166 | 147.941,65 | 1,30 | – |
| 2024-07 | 141 | 109.209,10 | -26,20 | – |
| 2024-08 | 99 | 97.482,35 | -10,70 | – |
| 2024-09 | 160 | 146.704,05 | 50,50 | – |
| 2024-10 | 185 | 178.004,80 | 21,30 | – |
| 2024-11 | 268 | 232.858,90 | 30,80 | – |
| 2024-12 | 327 | 325.005,15 | 39,60 | – |
| 2025-01 | 169 | 184.739,46 | -43,20 | 52,70 |
| 2025-02 | 149 | 139.224,64 | -24,60 | 17,50 |
| 2025-03 | 190 | 192.196,40 | 38,00 | 25,60 |
| 2025-04 | 181 | 140.833,08 | -26,70 | -29,70 |
| 2025-05 | 226 | 239.625,23 | 70,10 | 64,10 |
| 2025-06 | 203 | 182.496,84 | -23,80 | 23,40 |
| 2025-07 | 157 | 137.071,68 | -24,90 | 25,50 |
| 2025-08 | 133 | 155.586,29 | 13,50 | 59,60 |
| 2025-09 | 233 | 218.519,91 | 40,40 | 49,00 |
| 2025-10 | 216 | 215.671,60 | -1,30 | 21,20 |
| 2025-11 | 275 | 309.548,11 | 43,50 | 32,90 |
| 2025-12 | 341 | 295.143,20 | -4,70 | -9,20 |

**Conclusiones:**

- Las ventas pasaron de 1.975.927 € en 2024 a 2.410.656 € en 2025: un crecimiento del **22.0 %**.
- El mejor mes fue 2024-12 (325.005 €) y el peor 2024-08 (97.482 €).

## 3. Productos más vendidos

**Pregunta de negocio:** ¿Qué productos generan más ingresos y qué peso tienen sobre el total?  
**Consulta:** [`sql/analisis/03_top_productos.sql`](../sql/analisis/03_top_productos.sql)

| puesto | producto | categoria | unidades | ingresos | pct_ingresos | margen_pct |
|---|---|---|---|---|---|---|
| 1 | Smartphone Pro X | Electrónica | 756 | 639.151,69 | 14,60 | 7,60 |
| 2 | Portátil 14" | Informática | 590 | 549.488,46 | 12,50 | 15,70 |
| 3 | Televisor 55" | Electrónica | 728 | 441.101,29 | 10,10 | 3,80 |
| 4 | Smartphone Lite | Electrónica | 1185 | 386.278,26 | 8,80 | 1,70 |
| 5 | Portátil gaming | Informática | 256 | 355.455,62 | 8,10 | 11,70 |
| 6 | Tablet 10" | Electrónica | 826 | 229.775,22 | 5,20 | 3,00 |
| 7 | Monitor 27" | Informática | 734 | 190.436,05 | 4,30 | 13,70 |
| 8 | Smartwatch | Electrónica | 910 | 166.996,32 | 3,80 | 6,10 |
| 9 | Auriculares inalámbricos | Electrónica | 1367 | 164.454,23 | 3,70 | 7,70 |
| 10 | Robot aspirador | Hogar | 577 | 160.912,08 | 3,70 | 27,90 |
| 11 | Cafetera automática | Hogar | 431 | 139.303,35 | 3,20 | 30,20 |
| 12 | Freidora de aire | Hogar | 905 | 99.893,60 | 2,30 | 30,70 |
| 13 | Zapatillas running | Deportes | 886 | 89.716,21 | 2,00 | 34,00 |
| 14 | Altavoz inteligente | Electrónica | 1038 | 85.805,17 | 2,00 | 8,60 |
| 15 | Disco SSD 1TB | Informática | 853 | 78.270,44 | 1,80 | 13,20 |
| 16 | Bicicleta estática | Deportes | 194 | 71.472,47 | 1,60 | 33,60 |
| 17 | Teclado mecánico | Informática | 806 | 67.762,33 | 1,50 | 17,50 |
| 18 | Purificador de aire | Hogar | 281 | 48.798,67 | 1,10 | 31,00 |
| 19 | Chaqueta impermeable | Moda | 525 | 43.771,94 | 1,00 | 49,60 |
| 20 | Batidora de vaso | Hogar | 684 | 43.693,25 | 1,00 | 32,50 |
| 21 | Ratón ergonómico | Informática | 1161 | 42.056,16 | 1,00 | 11,90 |
| 22 | Vaqueros clásicos | Moda | 896 | 40.477,38 | 0,90 | 46,70 |
| 23 | Zapatos de piel | Moda | 439 | 40.106,93 | 0,90 | 47,80 |
| 24 | Mochila de senderismo | Deportes | 512 | 32.448,25 | 0,70 | 31,10 |
| 25 | Juego de sartenes | Hogar | 425 | 31.777,75 | 0,70 | 33,90 |

*Se muestran 25 de 37 filas.*

**Conclusiones:**

- Los 5 productos principales concentran el **54.1 %** de los ingresos; el líder es *Smartphone Pro X* (14.6 %).
- Ojo: entre los 10 más vendidos hay productos con margen inferior al 5 %: Televisor 55", Smartphone Lite, Tablet 10".

## 4. Rentabilidad por categoría

**Pregunta de negocio:** ¿Qué categorías venden más y cuáles dejan realmente más margen?  
**Consulta:** [`sql/analisis/04_categorias_margen.sql`](../sql/analisis/04_categorias_margen.sql)

| categoria | unidades | ingresos | beneficio_bruto | margen_pct | pct_ingresos | pct_beneficio | descuento_medio_pct |
|---|---|---|---|---|---|---|---|
| Electrónica | 6810 | 2.113.562,18 | 109.275,60 | 5,20 | 48,20 | 17,10 | 4,50 |
| Informática | 4400 | 1.283.469,06 | 181.085,39 | 14,10 | 29,30 | 28,40 | 4,50 |
| Hogar | 4083 | 549.754,52 | 164.277,83 | 29,90 | 12,50 | 25,80 | 4,50 |
| Deportes | 3059 | 239.784,47 | 81.429,56 | 34,00 | 5,50 | 12,80 | 4,90 |
| Moda | 3681 | 169.333,80 | 81.865,44 | 48,30 | 3,90 | 12,80 | 4,60 |
| Accesorios | 1439 | 30.679,36 | 19.531,00 | 63,70 | 0,70 | 3,10 | 4,50 |

**Conclusiones:**

- **Electrónica** genera el 48.2 % de los ingresos pero solo el 17.1 % del beneficio (margen del 5.2 %).
- La categoría que más beneficio aporta es **Informática** (181.085 €).
- **Accesorios** tiene el mayor margen (63.7 %) pero apenas representa el 0.7 % de las ventas: hay margen para crecer.

## 5. Ventas por región

**Pregunta de negocio:** ¿Qué regiones aportan más y cuánto vale de media un cliente en cada una?  
**Consulta:** [`sql/analisis/05_ventas_por_region.sql`](../sql/analisis/05_ventas_por_region.sql)

| region | clientes_registrados | clientes_compradores | pedidos | ingresos | ticket_medio | ingresos_por_cliente | pct_ingresos |
|---|---|---|---|---|---|---|---|
| Este | 85 | 83 | 1329 | 1.275.606,62 | 959,82 | 15.368,75 | 29,10 |
| Norte | 55 | 55 | 867 | 1.123.775,51 | 1.296,17 | 20.432,28 | 25,60 |
| Centro | 86 | 84 | 1196 | 1.043.478,59 | 872,47 | 12.422,36 | 23,80 |
| Sur | 39 | 37 | 551 | 517.443,99 | 939,10 | 13.984,97 | 11,80 |
| Oeste | 35 | 34 | 625 | 426.278,68 | 682,05 | 12.537,61 | 9,70 |

**Conclusiones:**

- **Este** lidera con el 29.1 % de los ingresos; **Oeste** queda última con el 9.7 %.
- En **Norte** cada cliente vale más de media (20.432 €).

## 6. Concentración de clientes (análisis de Pareto 80/20)

**Pregunta de negocio:** ¿Dependemos de pocos clientes? ¿Qué porcentaje de ingresos generan los mejores?  
**Consulta:** [`sql/analisis/06_top_clientes.sql`](../sql/analisis/06_top_clientes.sql)

| puesto | cliente | segmento | region | pedidos | ingresos | pct_ingresos | pct_acumulado | pct_clientes_acumulado |
|---|---|---|---|---|---|---|---|---|
| 1 | Grupo Rodríguez S.L. | Empresa | Norte | 181 | 361.531,75 | 8,20 | 8,20 | 0,30 |
| 2 | Talleres Álvarez S.L. | Empresa | Este | 179 | 314.613,46 | 7,20 | 15,40 | 0,70 |
| 3 | Servicios Fernández S.L. | Empresa | Sur | 64 | 130.960,91 | 3,00 | 18,40 | 1,00 |
| 4 | Soluciones Álvarez S.L. | Empresa | Norte | 39 | 118.806,36 | 2,70 | 21,10 | 1,40 |
| 5 | Distribuciones Gutiérrez S.L. | Empresa | Sur | 49 | 108.179,42 | 2,50 | 23,60 | 1,70 |
| 6 | Grupo Pérez S.L. | Empresa | Centro | 54 | 99.466,61 | 2,30 | 25,80 | 2,00 |
| 7 | Servicios López S.L. | Empresa | Este | 51 | 87.210,37 | 2,00 | 27,80 | 2,40 |
| 8 | Talleres Pérez S.L. | Empresa | Norte | 29 | 80.613,09 | 1,80 | 29,70 | 2,70 |
| 9 | Distribuciones Ortega S.L. | Empresa | Este | 46 | 74.055,97 | 1,70 | 31,40 | 3,10 |
| 10 | Soluciones Hernández S.L. | Empresa | Norte | 30 | 72.126,26 | 1,60 | 33,00 | 3,40 |
| 11 | Comercial Ortega S.L. | Empresa | Oeste | 37 | 62.769,08 | 1,40 | 34,40 | 3,80 |
| 12 | Talleres García S.L. | Empresa | Centro | 25 | 57.176,70 | 1,30 | 35,70 | 4,10 |
| 13 | Comercial Hernández S.L. | Empresa | Centro | 27 | 55.585,63 | 1,30 | 37,00 | 4,40 |
| 14 | Servicios Díaz S.L. | Empresa | Este | 22 | 54.312,47 | 1,20 | 38,20 | 4,80 |
| 15 | Ana Álvarez Fernández | Particular | Sur | 80 | 50.515,22 | 1,20 | 39,40 | 5,10 |
| 16 | Soluciones Muñoz S.L. | Empresa | Norte | 31 | 50.313,88 | 1,10 | 40,50 | 5,50 |
| 17 | Daniel Delgado López | Particular | Centro | 87 | 47.918,77 | 1,10 | 41,60 | 5,80 |
| 18 | Soluciones Rodríguez S.L. | Empresa | Centro | 29 | 47.770,16 | 1,10 | 42,70 | 6,10 |
| 19 | Distribuciones Fernández S.L. | Empresa | Centro | 13 | 45.342,44 | 1,00 | 43,80 | 6,50 |
| 20 | Beatriz Álvarez Jiménez | Particular | Este | 63 | 45.222,97 | 1,00 | 44,80 | 6,80 |
| 21 | Distribuciones Martín S.L. | Empresa | Norte | 23 | 44.280,88 | 1,00 | 45,80 | 7,20 |
| 22 | Servicios Rodríguez S.L. | Empresa | Este | 19 | 44.023,88 | 1,00 | 46,80 | 7,50 |
| 23 | Distribuciones Díaz S.L. | Empresa | Centro | 24 | 43.926,32 | 1,00 | 47,80 | 7,80 |
| 24 | Comercial Moreno S.L. | Empresa | Centro | 32 | 42.667,77 | 1,00 | 48,80 | 8,20 |
| 25 | Comercial Gómez S.L. | Empresa | Norte | 25 | 42.545,58 | 1,00 | 49,70 | 8,50 |

*Se muestran 25 de 293 filas.*

**Conclusiones:**

- El **20 % de los clientes genera el 72.2 %** de los ingresos.
- Solo los 3 primeros clientes suponen el 18.4 % de la facturación: hay un riesgo de dependencia elevado.
- 10 de los 10 mejores clientes son empresas.

## 7. Segmentación de clientes RFM

**Pregunta de negocio:** ¿Qué grupos de clientes tenemos según lo recientes, frecuentes y valiosos que son?  
**Consulta:** [`sql/analisis/07_segmentacion_rfm.sql`](../sql/analisis/07_segmentacion_rfm.sql)

| segmento_rfm | clientes | pct_clientes | ingresos | pct_ingresos | recencia_media_dias | pedidos_medios | gasto_medio |
|---|---|---|---|---|---|---|---|
| 1. Campeones | 36 | 12,30 | 1.780.211,04 | 40,60 | 4,00 | 48,20 | 49.450,31 |
| 2. Leales | 59 | 20,10 | 1.399.600,31 | 31,90 | 12,00 | 22,10 | 23.722,04 |
| 3. Recientes / potenciales | 51 | 17,40 | 205.596,75 | 4,70 | 10,00 | 5,00 | 4.031,31 |
| 4. En riesgo | 51 | 17,40 | 701.089,37 | 16,00 | 82,00 | 15,80 | 13.746,85 |
| 5. Inactivos | 96 | 32,80 | 300.085,94 | 6,80 | 145,00 | 4,80 | 3.125,90 |

**Conclusiones:**

- Los **Campeones** son el 12.3 % de los clientes y aportan el 40.6 % de los ingresos.
- Hay **51 clientes en riesgo** (compraban a menudo pero llevan ~82 días sin hacerlo) que representan 701.089 € de ingresos históricos.
- El 32.8 % de la cartera está inactiva.

## 8. Retención de clientes nuevos por cohorte

**Pregunta de negocio:** De los clientes que compran por primera vez cada trimestre, ¿cuántos vuelven a comprar?  
**Consulta:** [`sql/analisis/08_retencion_cohortes.sql`](../sql/analisis/08_retencion_cohortes.sql)

| cohorte | clientes_nuevos | repiten_90d_pct | repiten_180d_pct | repiten_365d_pct |
|---|---|---|---|---|
| 2024-T1 | 9 | 88,90 | 100,00 | 100,00 |
| 2024-T2 | 18 | 83,30 | 100,00 | 100,00 |
| 2024-T3 | 20 | 75,00 | 100,00 | 100,00 |
| 2024-T4 | 30 | 80,00 | 93,30 | 100,00 |
| 2025-T1 | 23 | 82,60 | 95,70 | – |
| 2025-T2 | 27 | 70,40 | 96,30 | – |
| 2025-T3 | 15 | 73,30 | – | – |
| 2025-T4 | 15 | – | – | – |

**Conclusiones:**

- De media, el **79.1 %** de los clientes nuevos repite compra en los primeros 90 días.
- A los 180 días la recompra sube al 97.5 %: la primera experiencia de compra funciona bien.

## 9. Estacionalidad por mes del año

**Pregunta de negocio:** ¿En qué meses se vende más y menos? ¿Cuánto se aleja cada mes de un mes medio?  
**Consulta:** [`sql/analisis/09_estacionalidad_mensual.sql`](../sql/analisis/09_estacionalidad_mensual.sql)

| mes | ingresos_medios_por_anio | indice_estacional |
|---|---|---|
| Enero | 152.850,13 | 84,00 |
| Febrero | 128.855,34 | 70,00 |
| Marzo | 172.587,35 | 94,00 |
| Abril | 170.541,24 | 93,00 |
| Mayo | 192.835,81 | 106,00 |
| Junio | 165.219,25 | 90,00 |
| Julio | 123.140,39 | 67,00 |
| Agosto | 126.534,32 | 69,00 |
| Septiembre | 182.611,98 | 100,00 |
| Octubre | 196.838,20 | 108,00 |
| Noviembre | 271.203,51 | 148,00 |
| Diciembre | 310.074,18 | 170,00 |

**Conclusiones:**

- **Diciembre** vende un 70 % más que un mes medio; **Julio** un 33 % menos.
- Noviembre y diciembre (Black Friday y Navidad) son la temporada clave.

## 10. Ventas por día de la semana

**Pregunta de negocio:** ¿Qué días de la semana concentran más pedidos?  
**Consulta:** [`sql/analisis/10_dia_semana.sql`](../sql/analisis/10_dia_semana.sql)

| dia | pedidos | ingresos | pct_pedidos |
|---|---|---|---|
| Lunes | 566 | 570.884,36 | 12,40 |
| Martes | 573 | 521.801,98 | 12,50 |
| Miércoles | 631 | 614.497,15 | 13,80 |
| Jueves | 601 | 546.412,48 | 13,20 |
| Viernes | 778 | 724.653,92 | 17,00 |
| Sábado | 898 | 909.368,46 | 19,70 |
| Domingo | 521 | 498.965,05 | 11,40 |

**Conclusiones:**

- **Sábado** y **Viernes** concentran el 36.7 % de los pedidos; Domingo es el día más flojo.

## 11. Rendimiento del equipo comercial

**Pregunta de negocio:** ¿Qué vendedores rinden por encima o por debajo de la media y cuántos pedidos pierden?  
**Consulta:** [`sql/analisis/11_rendimiento_vendedores.sql`](../sql/analisis/11_rendimiento_vendedores.sql)

| vendedor | region | pedidos_totales | cancelados_devueltos_pct | ingresos | ticket_medio | vs_media_pct |
|---|---|---|---|---|---|---|
| Elena Castro | Centro | 912 | 6,70 | 752.333,89 | 884,06 | 37,20 |
| Diego Torres | Este | 738 | 8,30 | 670.953,23 | 991,07 | 22,40 |
| Javier Ruiz | Norte | 482 | 6,20 | 628.781,95 | 1.391,11 | 14,70 |
| Lucía Navarro | Este | 706 | 7,60 | 604.653,39 | 927,38 | 10,30 |
| Marta Sánchez | Sur | 598 | 7,90 | 517.443,99 | 939,10 | -5,60 |
| Laura Gómez | Norte | 436 | 4,80 | 494.993,56 | 1.192,76 | -9,70 |
| Pablo Romero | Oeste | 686 | 8,90 | 426.278,68 | 682,05 | -22,30 |
| Sergio Molina | Centro | 442 | 21,90 | 291.144,70 | 843,90 | -46,90 |

**Conclusiones:**

- **Elena Castro** lidera el equipo (+37.2 % sobre la media).
- **Sergio Molina** factura un 46.9 % menos que la media y tiene un 21.9 % de pedidos cancelados o devueltos (media del equipo: 9.0 %).

## 12. Productos sin ventas

**Pregunta de negocio:** ¿Hay productos en catálogo que nunca se han vendido?  
**Consulta:** [`sql/analisis/12_productos_sin_ventas.sql`](../sql/analisis/12_productos_sin_ventas.sql)

| producto | categoria | precio | coste | margen_teorico_pct |
|---|---|---|---|---|
| Pulsómetro | Deportes | 79,00 | 49,95 | 36,80 |
| Cámara deportiva | Electrónica | 249,00 | 227,35 | 8,70 |
| Impresora multifunción | Informática | 159,00 | 122,11 | 23,20 |

**Conclusiones:**

- Hay **3 productos que nunca se han vendido**: Pulsómetro, Cámara deportiva, Impresora multifunción. Conviene revisarlos o retirarlos del catálogo.

## 13. Recomendaciones para la empresa

1. **Revisar precios y descuentos en Electrónica**: es la categoría que más factura pero la que menos margen deja (5.2 %).
2. **Impulsar la venta cruzada de Accesorios** (margen del 63.7 %) junto a los productos más vendidos.
3. **Lanzar una campaña de reactivación** para los 51 clientes en riesgo antes de perderlos.
4. **Crear un programa de cuentas clave** para los mejores clientes: unos pocos concentran gran parte de la facturación y su pérdida tendría un gran impacto.
5. **Planificar stock, personal y campañas** para noviembre-diciembre y aprovechar la caída de julio-agosto para promociones.
6. **Analizar los pedidos fallidos de Sergio Molina** y reforzar su formación o seguimiento.
7. **Revisar los productos sin ventas** para liberar catálogo y stock inmovilizado.
