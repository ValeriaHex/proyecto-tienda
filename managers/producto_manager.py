from modelos.producto import Producto

productos = []
def agregar_productos():
	nombre = input(" Nombre del producto: ")
	codigo = input(" Codigo/ID: ")
	precio = float(input(" Precio: "))
	talla = input(" Talla: ")
	color = input(" Color: ")
	categoria = input(" Categoria: ")
	cantidad = int(input(" Cantidad disponible: "))

	producto = Producto(codigo, nombre, precio, talla, color, categoria, cantidad)
	productos.append(producto)
	print(f" Producto '{nombre}' agregado correctamente.")

def listar_productos():
	if not productos:
		print(" No hay productos registrados.")
		return
	print("\n -------- Lista de Productos --------")
	for p in productos:
		print(p)


