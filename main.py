import os
from datetime import datetime
from managers.producto_manager import *
from managers.cliente_manager import *
from managers.venta_manager import *
from managers.inventario_manager import *

def mostrar_menu():
	os.system('cls')
	print(" ---------------- Tienda ----------------")
	print("  1. Gestionar Productos")
	print("  2. Gestionar Clientes")
	print("  3. Gestionar ventas")
	print("  4. Gestionar inventario")
	print("  5. Salir")
	print(" ----------------------------------------")
	op = input(" Seleccione una opcion: ")
	return op
while True:
	op = mostrar_menu()

	if op == "1":
	  print(" 1. Agregar producto")
	  print(" 2. Listar productos")
	  sub = input(" Elige: ")
	  if sub == "1":
	    agregar_productos()
	  elif sub == "2":
	    listar_productos()
	  input(" Presiona Enter para continuar...")

	elif op == "2":
	  print(" 1. Agregar cliente")
	  print(" 2. Listar Clientes")
	  sj = input(" Elige: ")
	  if sj == "1":
	    agregar_clientes()
	  elif sj == "2":
	    listar_clientes()
	  input(" Presiona Enter para continuar...")

	elif op == "3":
	  print(" 1. Registrar venta")
	  print(" 2. Listar ventas")
	  sb = input(" Elige: ")
	  if sb == "1":
	    registrar_venta(productos)
	  elif sb == "2":
	    listar_ventas()
	  input(" Presiona Enter para continuar...")

	elif op == "4":
	  print(" 1. Mostrar inventario")
	  print(" 2. Actualizar stock")
	  si = input(" Elige: ")
	  if si == "1":
	    mostrar_inventario(productos)
	  elif si == "2":
	    actualizar_stock(productos)
	  input(" Presiona Enter para continuar...")

	elif op == "5":
	  print(" Saliendo...")
	  break

	else:
	  print(" Opción no válida.")
	  input(" Presiona Enter para continuar...")
