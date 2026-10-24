"""Sistema de análisis de ventas con SQL.

Pasos:
  1. Crea la base de datos SQLite (ventas.db) con su esquema y vistas.
  2. La llena con datos ficticios generados por src/generar_datos.py.
  3. Ejecuta todas las consultas de sql/analisis/.
  4. Genera el informe reports/informe.md con tablas y conclusiones.

Uso:  python3 main.py
"""

from src import base_datos as bd
from src.generar_datos import generar_datos
from src.informe import conclusiones, generar_informe

RUTA_BD = bd.RAIZ / "ventas.db"
RUTA_INFORME = bd.RAIZ / "reports" / "informe.md"


def main():
    print("1. Creando la base de datos...")
    RUTA_BD.unlink(missing_ok=True)
    conexion = bd.conectar(RUTA_BD)
    bd.crear_esquema(conexion)

    print("2. Generando y cargando datos...")
    datos = generar_datos()
    bd.cargar_datos(conexion, datos)
    for tabla in bd.ORDEN_TABLAS:
        print(f"   - {tabla}: {len(datos[tabla])} filas")

    print("3. Ejecutando consultas de análisis...")
    resultados = bd.ejecutar_analisis(conexion)
    conexion.close()

    print("4. Generando informe...")
    RUTA_INFORME.parent.mkdir(exist_ok=True)
    RUTA_INFORME.write_text(generar_informe(resultados), encoding="utf-8")

    print("\nConclusiones principales:")
    for nombre in ("01_kpis_generales", "04_categorias_margen", "06_top_clientes"):
        for frase in conclusiones(resultados)[nombre]:
            print(f"  • {frase.replace('**', '').replace('*', '')}")

    print(f"\nBase de datos: {RUTA_BD.relative_to(bd.RAIZ)}")
    print(f"Informe completo: {RUTA_INFORME.relative_to(bd.RAIZ)}")


if __name__ == "__main__":
    main()
