from conexion import DB_PATH
import sqlite3

print("Base de datos usada:", DB_PATH)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("📋 Tablas en la base de datos:")
for tabla in cursor.fetchall():
	print("-", tabla[0])

conn.close()
