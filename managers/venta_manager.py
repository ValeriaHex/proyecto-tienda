from datetime import datetime

ventas = []
def registrar_venta(prod_disp):
	if len(prod_disp) == 0:
	  print(" No hay productos disponibles para vender.")
	  return

	carrito = [] #productos comprados en esta venta
	total = 0

	while True:
	  print("\n ------ Lista de Productos Disponibles ------")

	  for i, prod in enumerate(prod_disp):
	    print(f" {i+1}. {prod['nombre']} - ${prod['precio']} - (Stock: {prod['cantidad']})")

	  elec = input(" Elige el número del producto (o 0 para terminar): ")

	  if elec == "0":
	    break

	  try:
	    indice = int(elec) - 1
	    if indice < 0 or indice >= len(prod_disp):
	      print(" Opción inválida.")
	      continue

	    producto = prod_disp[indice]

	    #verificar stock
	    cantidad = int(input(f" Cantidad de {producto['nombre']}: "))
	    if cantidad > producto['cantidad']:
	      print("No hay suficiente stock.")
	      continue

	    #Calcular subtotal
	    subtotal = producto['precio'] * cantidad
	    total += subtotal

	    #Guardar en el carrito
	    carrito.append({"nombre": producto['nombre'], "cantidad": cantidad, "precio_unitario": producto['precio'], "subtotal": subtotal})

	    #Actualizar stock del producto
	    producto['cantidad'] -= cantidad

	  except ValueError:
	      print(" Se debe ingresar un número válido.")
	if len(carrito) == 0:
	  print(" No se registró ninguna venta.")
	  return

	venta = {
		"productos": carrito,
		"total": total,
		"fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	}
	ventas.append(venta)
	print("\n ¡Venta registrada con éxito!")
	print(f" Total de la venta: ${total}")

def listar_ventas():
	if len(ventas) == 0:
	  print(" No hay ventas registradas.")
	  return
	print("\n -------- Historial de Ventas --------")
	for i, v in enumerate(ventas):
	  print(f"\n Venta {i+1} - Fecha: {v['fecha']}")
	  for item in v["productos"]:
	    print(f" {item['cantidad']} x {item['nombre']} -> ${item['precio_unitario']} = ${item['subtotal']}")
	  print(f" Total: ${v['total']}")
