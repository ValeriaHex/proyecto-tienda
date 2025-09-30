from consola.menu import mostrar_menu
from managers.producto_manager import agregar_productos, listar_productos
from managers.cliente_manager import agregar_clientes, listar_clientes
from managers.venta_manager import registrar_venta, listar_ventas
from managers.inventario_manager import mostrar_inventario, actualizar_stock

while True:
	op = mostrar_menu()

	if op == "1":
	  print("    1. Agregar producto")
	  print("    2. Listar productos")
	  sub = input(" ❣ Elige: ")
	  if sub == "1":
	    agregar_productos()
	  elif sub == "2":
	    listar_productos()
	  input("\n Presiona Enter para continuar...")

	elif op == "2":
	  print("    1. Agregar cliente")
	  print("    2. Listar Clientes")
	  sj = input(" ❣ Elige: ")
	  if sj == "1":
	    agregar_clientes()
	  elif sj == "2":
	    listar_clientes()
	  input("\n Presiona Enter para continuar...")

	elif op == "3":
	  print("    1. Registrar venta")
	  print("    2. Listar ventas")
	  sb = input(" ❣ Elige: ")
	  if sb == "1":
	    registrar_venta()
	  elif sb == "2":
	    listar_ventas()
	  input("\n Presiona Enter para continuar...")

	elif op == "4":
	  print("    1. Mostrar inventario")
	  print("    2. Actualizar stock")
	  si = input(" ❣ Elige: ")
	  if si == "1":
	    mostrar_inventario()
	  elif si == "2":
	    actualizar_stock()
	  input("\n Presiona Enter para continuar...")

	elif op == "5":
	  print(" 🌈 Saliendo...")
	  break

	else:
	  print(" ⚠ Opción no válida.")
	  input("\n Presiona Enter para continuar...")
