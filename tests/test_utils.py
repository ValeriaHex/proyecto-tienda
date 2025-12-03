import tempfile
import os
import database.conexion as conexion
import database.tablas as tablas
from database.conexion import get_db_connection, DB_PATH

def crear_db_temporal():
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    tmp.close()
    conexion.DB_PATH = tmp.name 
    tablas.crear_tablas()
    return tmp.name

def borrar_db(path):
    try:
        os.remove(path)
    except Exception:
        pass