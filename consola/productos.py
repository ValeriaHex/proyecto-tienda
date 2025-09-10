productos = []
def agregar_productos():
	nombre = input("Nombre del producto: ")
	codigo = input("Codigo/ID: ")
	precio = float(input("Precio: "))
	talla = input("Talla: ")
	color = input("Color: ")
	categoria = input("Categoria: ")
	cantidad = int(input("Cantidad disponible: "))
	producto = {
	  "nombre": nombre,
	  "codigo": codigo,
	  "precio": precio,
	  "talla": talla,
	  "color": color,
	  "categoria": categoria,
	  "cantidad": cantidad
	}
	productos.append(producto)
	print(f"Producto {nombre} agregado correctamente.")
def listar_productos():
	if not productos:
		print("No hay productos registrados.")
		return
	for p in productos:
		print(f"{p['codigo']} - {p['nombre']} | Precio: ${p['precio']} | Cantidad: {p['cantidad']}")


