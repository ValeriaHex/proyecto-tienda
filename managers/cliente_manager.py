from modelos.cliente import Cliente
from database.conexion import get_db_connection
from datetime import datetime

def agregar_clientes():
	print("\n  📋 Registrar nuevo cliente")
	print("──────────────────────────────────────────────")
	nombre = input(" 🔤 Nombre del cliente: ")
	correo = input(" 📧 Correo del cliente: ")
	direccion = input(" 🏠 Dirrecion de envío: ")

	cliente = Cliente(nombre, correo, direccion)

	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute(
	  "INSERT INTO clientes (nombre, correo, direccion, fecha_registro) VALUES (?, ?, ?, ?)",
	  (cliente.nombre, cliente.correo, cliente.direccion, cliente.fecha_registro)
	)
	conn.commit()
	conn.close()
	print(f" ✅ Cliente '{nombre}' agregado correctamente.")
	print("──────────────────────────────────────────────\n")

def listar_clientes():
	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM clientes")
	filas = cursor.fetchall()
	conn.close()

	if not filas:
		print(" ⛔ No hay clientes registrados.")
		return
	print("\n 📋 Lista de clientes ")
	print("────────────────────────────────────────────────────────────────────────────────────────────────")
	print(f" {'ID':<3} {'Nombre':<14} {'Correo':<18} {'Dirección':<27} {'Fecha Registro'}")
	print("────────────────────────────────────────────────────────────────────────────────────────────────")

	#for i, fila in enumerate(filas, 1):
	#	print(f" {i}. {fila['nombre']} - {fila['correo']} - {fila['direccion']} - {fila['fecha_registro']}")
	for fila in filas:
		print(f" {fila['id']:<3} {fila['nombre']:<14} {fila['correo']:<18} {fila['direccion']:<27} {fila['fecha_registro']}")
    
	print("────────────────────────────────────────────────────────────────────────────────────────────────\n")


