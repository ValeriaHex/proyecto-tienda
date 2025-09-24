def mostrar_inventario(productos):
	if len(productos) == 0:
	  print(" No hay productos en el inventario.")
	  return

	print("\n -------- Inventario de Productos --------")
	for p in productos:
	  print(f" Nombre: {p['nombre']}, Precio: ${p['precio']}, Stock: {p['cantidad']}")

def actualizar_stock(productos):
	if len(productos) == 0:
	  print(" No hay productos para actualizar.")
	  return

	print("\n -------- Actualizar Stock --------")
	for i, p in enumerate(productos):
	  print(f" {i+1}. {p['nombre']} - Stock actual: {p['cantidad']}")

	try:
	  op = int(input(" Elige el número del producto")) - 1
	  if op<0 or op>=len(productos):
	    print(" Opción inválida.")
	    return
	  nuevo_stock = int(input(" Nuevo stock para este producto: "))
	  productos[op]['cantidad'] = nuevo_stock
	  print(" ¡Stock actualizado con éxito!")

	except ValueError:
	  print(" Debes ingresar un número válido.")
