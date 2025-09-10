import os
from datetime import datetime
from productos import *
from clientes import *
from ventas import *
from inventario import *

def mostrar_menu():
	os.system('cls')
	print("---- Tienda ----")
	print("1. Gestionar Productos")
	print("2. Salir")
	op = input("Seleccione una opcion: ")
	return op
while True:
	op = mostrar_menu()
	if op == "1":
	  print("1. Agregar producto")
	  print("2. Listar productos")
	  sub = input("Elige: ")
	  if sub == "1":
	    agregar_productos()
	  elif sub == "2":
	    listar_productos()
	  input("Presiona Enter para continuar...")
	elif op == "2":
	  print("Saliendo...")
	  break
	else:
	  print("Opción no válida.")
	  input("Presiona Enter para continuar...")
