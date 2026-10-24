"""Funciones para trabajar con la base de datos SQLite."""

import sqlite3
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CARPETA_SQL = RAIZ / "sql"
CARPETA_ANALISIS = CARPETA_SQL / "analisis"

# Orden de carga: primero las tablas de las que dependen las demás (claves foráneas)
ORDEN_TABLAS = ["regiones", "categorias", "productos", "vendedores",
                "clientes", "pedidos", "detalle_pedidos"]


def conectar(ruta=":memory:"):
    """Abre una conexión con las claves foráneas activadas."""
    conexion = sqlite3.connect(ruta)
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def ejecutar_script(conexion, ruta_sql):
    """Ejecuta un archivo .sql completo (puede tener varias sentencias)."""
    conexion.executescript(Path(ruta_sql).read_text(encoding="utf-8"))


def crear_esquema(conexion):
    ejecutar_script(conexion, CARPETA_SQL / "01_esquema.sql")
    ejecutar_script(conexion, CARPETA_SQL / "02_vistas.sql")


def cargar_datos(conexion, datos):
    """Inserta los datos de cada tabla dentro de una única transacción."""
    with conexion:  # confirma al final o deshace todo si hay un error
        for tabla in ORDEN_TABLAS:
            filas = datos[tabla]
            marcadores = ", ".join("?" * len(filas[0]))
            conexion.executemany(f"INSERT INTO {tabla} VALUES ({marcadores})", filas)


def consultar(conexion, sql):
    """Ejecuta una consulta y devuelve (nombres de columnas, filas)."""
    cursor = conexion.execute(sql)
    columnas = [descripcion[0] for descripcion in cursor.description]
    return columnas, cursor.fetchall()


def leer_analisis(ruta_sql):
    """Lee un archivo de análisis: su título, la pregunta de negocio y la consulta.

    La cabecera de cada archivo sigue este formato:
        -- Título: ...
        -- Pregunta: ...
    """
    texto = Path(ruta_sql).read_text(encoding="utf-8")
    titulo, pregunta = Path(ruta_sql).stem, ""
    for linea in texto.splitlines():
        if linea.startswith("-- Título:"):
            titulo = linea.split(":", 1)[1].strip()
        elif linea.startswith("-- Pregunta:"):
            pregunta = linea.split(":", 1)[1].strip()
    return titulo, pregunta, texto


def ejecutar_analisis(conexion):
    """Ejecuta todas las consultas de sql/analisis en orden.

    Devuelve un diccionario {nombre_archivo: resultado}.
    """
    resultados = {}
    for ruta in sorted(CARPETA_ANALISIS.glob("*.sql")):
        titulo, pregunta, sql = leer_analisis(ruta)
        columnas, filas = consultar(conexion, sql)
        resultados[ruta.stem] = {
            "titulo": titulo,
            "pregunta": pregunta,
            "columnas": columnas,
            "filas": filas,
        }
    return resultados
