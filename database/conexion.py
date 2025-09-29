import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DB_PATH = os.path.join(BASE_DIR, "tienda.db")

def get_db_connection():
	conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
	conn.row_factory = sqlite3.Row
	conn.execute("PRAGMA foreign_keys = ON;")
	return conn

if __name__ == "__main__":
	conn = get_db_connection()
	print("Conexión OK - archivo DB: ", DB_PATH)
	conn.close()
