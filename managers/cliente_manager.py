from modelos.cliente import Cliente
from database.conexion import get_db_connection
from datetime import datetime

def agregar_clientes():
	print("\n  📋 Registrar nuevo cliente")
	print("─────────────────────────────────────────────────")
	nombre = input(" 🔤 Nombre del cliente: ")
	correo = input(" 📧 Correo del cliente: ")
	direccion = input(" 🏠 Direccion de envío: ")

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
	print("─────────────────────────────────────────────────\n")

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
	print("───────────────────────────────────────────────────────────────────────────────────────────────")
	print(f" {'ID':<3} {'Nombre':<15} {'Correo':<20} {'Dirección':<25} {'Fecha Registro'}")
	print("───────────────────────────────────────────────────────────────────────────────────────────────")

	#for i, fila in enumerate(filas, 1):
	#	print(f" {i}. {fila['nombre']} - {fila['correo']} - {fila['direccion']} - {fila['fecha_registro']}")
	for fila in filas:
		print(f" {fila['id']:<3} {fila['nombre']:<15} {fila['correo']:<20} {fila['direccion']:<25} {fila['fecha_registro']}")

	print("───────────────────────────────────────────────────────────────────────────────────────────────\n")

def eliminar_cliente():
	from database.conexion import get_db_connection
	import os

	conn = get_db_connection()
	cursor = conn.cursor()

	try:
		cursor.execute("SELECT id, nombre, correo, direccion FROM clientes ORDER BY id")
		clientes = cursor.fetchall()

		if not clientes:
			print("\n ⛔ No hay clientes registrados.")
			conn.close()
			return

		print("\n 📋 Lista de clientes ")
		print("────────────────────────────────────────────────────────────────")
		print(f" {'ID':<3} {'Nombre':<15} {'Correo':<20} {'Dirección'}")
		print("────────────────────────────────────────────────────────────────")
		for c in clientes:
			print(f" {c['id']:<3} {c['nombre']:<15} {c['correo']:<20} {c['direccion']}")
		print("────────────────────────────────────────────────────────────────")

		# Pedir el ID de la ventan a eliminar
		cliente_id = input("\n 💬 ID del cliente a eliminar: ")

		# Verificar que exista
		cursor.execute("SELECT id FROM clientes WHERE id = ?", (cliente_id,))
		cliente = cursor.fetchone()

		if cliente:
			confirmar = input(f" Está seguro de eliminar al cliente ID {cliente_id}? (s/n): ").lower()
			if confirmar == "s":
				cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
				conn.commit()
				print("\n ✅ Cliente eliminado correctamente.")
			else:
				print("\n ❌ Operación cancelada.")
		else:
			print("\n ⚠ No existe ningun cliente con ese ID.")

	except Exception as e:
		print(" ⚠ Error al eliminar la venta:", e)
	finally:
		conn.close()
