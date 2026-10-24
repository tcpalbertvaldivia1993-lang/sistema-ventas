"""Pruebas del sistema: integridad del esquema y coherencia de los análisis.

Ejecutar desde la raíz del proyecto:  python3 -m unittest discover tests -v
"""

import sqlite3
import unittest

from src import base_datos as bd
from src.generar_datos import generar_datos
from src.informe import generar_informe


class TestEsquema(unittest.TestCase):
    """Comprueba que las restricciones de la base de datos funcionan."""

    def setUp(self):
        self.conexion = bd.conectar()
        bd.crear_esquema(self.conexion)
        self.conexion.execute("INSERT INTO regiones VALUES (1, 'Norte')")
        self.conexion.execute("INSERT INTO categorias VALUES (1, 'Hogar')")
        self.conexion.execute("INSERT INTO productos VALUES (1, 'Lámpara', 1, 30, 10)")
        self.conexion.execute("INSERT INTO vendedores VALUES (1, 'Ana', 1)")
        self.conexion.execute(
            "INSERT INTO clientes VALUES (1, 'Luis', 'luis@ejemplo.com', 1, '2024-01-01', 'Particular')")
        self.conexion.execute("INSERT INTO pedidos VALUES (1, 1, 1, '2024-02-01', 'completado')")

    def tearDown(self):
        self.conexion.close()

    def test_clave_foranea_rechaza_cliente_inexistente(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.conexion.execute("INSERT INTO pedidos VALUES (2, 999, 1, '2024-02-01', 'completado')")

    def test_cantidad_debe_ser_positiva(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.conexion.execute("INSERT INTO detalle_pedidos VALUES (1, 1, 0, 30, 0)")

    def test_estado_no_valido(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.conexion.execute("INSERT INTO pedidos VALUES (2, 1, 1, '2024-02-01', 'perdido')")

    def test_precio_mayor_que_coste(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.conexion.execute("INSERT INTO productos VALUES (2, 'Mesa', 1, 10, 20)")

    def test_email_unico(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.conexion.execute(
                "INSERT INTO clientes VALUES (2, 'Otro', 'luis@ejemplo.com', 1, '2024-01-01', 'Empresa')")

    def test_vista_calcula_importe_neto(self):
        self.conexion.execute("INSERT INTO detalle_pedidos VALUES (1, 1, 2, 30, 0.10)")
        importe, coste = self.conexion.execute(
            "SELECT importe_neto, coste_total FROM v_ventas_detalle").fetchone()
        self.assertAlmostEqual(importe, 54.0)  # 2 x 30 con 10 % de descuento
        self.assertAlmostEqual(coste, 20.0)


class TestAnalisis(unittest.TestCase):
    """Carga los datos generados una sola vez y comprueba los resultados."""

    @classmethod
    def setUpClass(cls):
        cls.conexion = bd.conectar()
        bd.crear_esquema(cls.conexion)
        bd.cargar_datos(cls.conexion, generar_datos())
        cls.resultados = bd.ejecutar_analisis(cls.conexion)

    @classmethod
    def tearDownClass(cls):
        cls.conexion.close()

    def columna(self, analisis, nombre):
        res = self.resultados[analisis]
        indice = res["columnas"].index(nombre)
        return [fila[indice] for fila in res["filas"]]

    def test_datos_respetan_claves_foraneas(self):
        self.assertEqual(self.conexion.execute("PRAGMA foreign_key_check").fetchall(), [])

    def test_todas_las_consultas_devuelven_filas(self):
        self.assertEqual(len(self.resultados), 12)
        for nombre, res in self.resultados.items():
            with self.subTest(analisis=nombre):
                self.assertTrue(res["filas"], f"{nombre} no devuelve filas")
                self.assertTrue(res["pregunta"], f"{nombre} no tiene pregunta de negocio")

    def test_suma_mensual_igual_a_ingresos_totales(self):
        total = self.columna("01_kpis_generales", "ingresos")[0]
        self.assertAlmostEqual(sum(self.columna("02_ventas_mensuales", "ingresos")), total, delta=1)

    def test_suma_por_categoria_y_region_igual_al_total(self):
        total = self.columna("01_kpis_generales", "ingresos")[0]
        self.assertAlmostEqual(sum(self.columna("04_categorias_margen", "ingresos")), total, delta=1)
        self.assertAlmostEqual(sum(self.columna("05_ventas_por_region", "ingresos")), total, delta=1)

    def test_pareto_acumulado_termina_en_100(self):
        acumulado = self.columna("06_top_clientes", "pct_acumulado")
        self.assertEqual(acumulado[-1], 100.0)
        self.assertEqual(acumulado, sorted(acumulado))

    def test_segmentos_rfm_cubren_todos_los_clientes(self):
        activos = self.columna("01_kpis_generales", "clientes_activos")[0]
        self.assertEqual(sum(self.columna("07_segmentacion_rfm", "clientes")), activos)

    def test_productos_sin_ventas_detectados(self):
        sin_ventas = set(self.columna("12_productos_sin_ventas", "producto"))
        self.assertEqual(sin_ventas, {"Cámara deportiva", "Impresora multifunción", "Pulsómetro"})

    def test_informe_contiene_todas_las_secciones(self):
        informe = generar_informe(self.resultados)
        for res in self.resultados.values():
            self.assertIn(res["titulo"], informe)
        self.assertIn("Recomendaciones para la empresa", informe)


if __name__ == "__main__":
    unittest.main()
