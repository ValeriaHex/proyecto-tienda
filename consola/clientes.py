import os
from datetime import datetime

clientes = []
def agregar_clientes():
	nombre = input(" Nombre del cliente: ")
	correo = input(" Correo del cliente: ")
	direccion = input(" Dirrecion de envío: ")
	cliente = {
	  "nombre":nombre,
	  "correo":correo,
	  "direccion":direccion,
	  "fecha_registro":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	}
	clientes.append(cliente)
	print(f" Cliente '{nombre}' agregado correctamente.")
def listar_clientes():
	if not clientes:
		print(" No hay clientes registrados.")
		return
	print("\n -------- Lista de clientes --------")
	for i, cliente in enumerate(clientes, 1):
		print(f" {i}. {cliente['nombre']} - {cliente['correo']} - {cliente['direccion']} - {cliente['fecha_registro']}")



