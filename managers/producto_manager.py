from modelos.producto import Producto
from database.conexion import get_db_connection

def agregar_productos():
  print("\n 🆕 Registrar nuevo producto")
  print("─────────────────────────────────────────────────")
  nombre = input(" 🔤 Nombre del producto: ")
  precio = float(input(" 💲 Precio: "))
  talla = input(" 📏 Talla: ")
  color = input(" 🎨 Color: ")
  categoria = input(" 📂 Categoria: ")
  cantidad = int(input(" 📦 Cantidad disponible: "))

  producto = Producto(nombre, precio, talla, color, categoria, cantidad)
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute(
	  "INSERT INTO productos (nombre, precio, talla, color, categoria, cantidad) VALUES (?, ?, ?, ?, ?, ?)",
    (producto.nombre, producto.precio, producto.talla, producto.color, producto.categoria, producto.cantidad)
  )
  conn.commit()
  conn.close()
  print(f" ✅ Producto '{nombre}' agregado correctamente.")
  print("─────────────────────────────────────────────────")

def listar_productos():
	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM productos")
	filas = cursor.fetchall()
	conn.close()

	if not filas:
		print(" ⛔ No hay productos registrados.")
		return

	print("\n 📋 Lista de Productos")
	print("──────────────────────────────────────────────────────────────────────────────")
	print(f" {'ID':<4} {'Nombre':<20} {'Precio':<10} {'Stock':<8} {'Talla':<8} {'Color':<10} {'Categoría'}")
	print("──────────────────────────────────────────────────────────────────────────────")

	for fila in filas:
		#print(f" {fila['id']} - {fila['nombre']} | Precio: ${fila['precio']} | Stock: {fila['cantidad']}")
		print(f" {fila['id']:<4} {fila['nombre']:<20} ${fila['precio']:<9.2f} {fila['cantidad']:<8} {fila['talla'] or '-':<8} {fila['color'] or '-':<10} {fila['categoria'] or '-'}")
	print("──────────────────────────────────────────────────────────────────────────────\n")


