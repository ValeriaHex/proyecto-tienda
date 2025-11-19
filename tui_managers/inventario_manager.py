from database.conexion import get_db_connection

def mostrar_inventario():
	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM productos")
	productos = cursor.fetchall()
	conn.close()

	if not productos:
		print(" ⛔ No hay productos en el inventario.")
		return

	print("\n 📦 Inventario de Productos")
	print("─────────────────────────────────────────────────────────────────────────────")
	print(f" {'ID':<4} {'Nombre':<20} {'Precio':<10} {'Stock':<7} {'Talla':<8} {'Color':<10} {'Categoría'}")
	print("─────────────────────────────────────────────────────────────────────────────")


	for p in productos:
		#print(f" {p['id']} - {p['nombre']} | Precio: ${p['precio']} | Stock: {p['cantidad']}")
		print(f" {p['id']:<4} {p['nombre']:<20} ${p['precio']:<9.2f} {p['cantidad']:<7} {p['talla'] or '-':<8} {p['color'] or '-':<10} {p['categoria'] or '-'}")

	print("─────────────────────────────────────────────────────────────────────────────\n")

def actualizar_stock():
	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT* FROM productos")
	productos = cursor.fetchall()

	if not productos:
		print(" ⛔ No hay productos para actualizar.")
		conn.close()
		return

	print("\n 🔧 Actualizar Stock")
	print("─────────────────────────────────────────")
	for i, p in enumerate(productos, 1):
		nom_formateado = p['nombre'].ljust(18)
		print(f" {i}. {nom_formateado} (Stock actual: {p['cantidad']})")
	print("─────────────────────────────────────────")

	try:
		op = int(input(" ❣ Elige el número del producto: ")) - 1
		if op < 0 or op >= len(productos):
			print(" ⚠ Opción inválida.")
			conn.close()
			return

		nuevo_stock = int(input(" 📦 Nuevo stock: "))
		producto_id = productos[op]['id']
		cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nuevo_stock, producto_id))
		conn.commit()
		conn.close()
		print("\n ✅ ¡Stock actualizado con éxito!")

	except ValueError:
		print(" ⚠ Debes ingresar un número válido.")
		conn.close()
