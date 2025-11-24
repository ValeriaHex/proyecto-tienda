import curses
from database.conexion import get_db_connection
from modelos.producto import Producto
from curses import textpad

def input_box(stdscr, prompt):
  curses.curs_set(1)
  stdscr.clear()
  h, w = stdscr.getmaxyx()

  titulo = "🆕 REGISTRAR NUEVO PRODUCTO"
  separador = "─" * (len(titulo) + 4)
  stdscr.addstr(1, max(2, w//2 - len(titulo)//2), titulo)
  stdscr.addstr(2, max(2, w//2 - len(separador)//2), separador)
  stdscr.refresh()

  texto = prompt[:w-4]
  stdscr.addstr(3, 2, texto)
  stdscr.refresh()

  win = curses.newwin(3, w-4, 4, 2)
  win.box()
  win.refresh()

  curses.echo()
  ui = win.getstr(1, 1, w-6).decode("utf-8")
  curses.noecho()

  return ui

def agregar_productos_tui(stdscr):
  stdscr.clear()
  h, w = stdscr.getmaxyx()
  
  nombre = input_box(stdscr, "🔤 Nombre del producto: ")
  precio = input_box(stdscr, "💲 Precio: ")
  talla = input_box(stdscr, "📏 Talla: ")
  color = input_box(stdscr, "🎨 Color: ")
  categoria = input_box(stdscr, "📂 Categoria: ")
  cantidad = input_box(stdscr, "📦 Cantidad disponible: ")
  
  try:
    precio = float(precio)
    cantidad = int(cantidad)
  except ValueError:
     stdscr.addstr(12, 2, "⚠ Error: Precio o cantidad no válidos")
     stdscr.getch()
     return
  
  producto = Producto(nombre, precio, talla, color, categoria, cantidad)
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute(
	  "INSERT INTO productos (nombre, precio, talla, color, categoria, cantidad) VALUES (?, ?, ?, ?, ?, ?)",
    (producto.nombre, producto.precio, producto.talla, producto.color, producto.categoria, producto.cantidad)
  )
  conn.commit()
  conn.close()

  stdscr.addstr(8, 2, f"✅ Producto '{nombre}' agregado correctamente.")
  stdscr.refresh()
  stdscr.getch()

def listar_productos():
	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM productos")
	filas = cursor.fetchall()
	conn.close()

	if not filas:
		print(" ⛔ No hay productos registrados.")
		return

	print("\n 📋 LISTA DE PRODUCTOS ")
	print("──────────────────────────────────────────────────────────────────────────────")
	print(f" {'ID':<4} {'Nombre':<20} {'Precio':<10} {'Stock':<8} {'Talla':<8} {'Color':<10} {'Categoría'}")
	print("──────────────────────────────────────────────────────────────────────────────")

	for fila in filas:
		#print(f" {fila['id']} - {fila['nombre']} | Precio: ${fila['precio']} | Stock: {fila['cantidad']}")
		print(f" {fila['id']:<4} {fila['nombre']:<20} ${fila['precio']:<9.2f} {fila['cantidad']:<8} {fila['talla'] or '-':<8} {fila['color'] or '-':<10} {fila['categoria'] or '-'}")
	print("──────────────────────────────────────────────────────────────────────────────\n")

def eliminar_producto_tui(stdscr):
  curses.curs_set(0)
  conn = get_db_connection()
  cursor = conn.cursor()
  
  cursor.execute("SELECT id, nombre, precio, cantidad FROM productos ORDER BY id")
  productos = cursor.fetchall()
  
  if not productos:
    stdscr.clear()
    stdscr.addstr(2, 2, "⛔ No hay productos registrados.")
    stdscr.refresh()
    stdscr.getch()
    conn.close()
    return
  
  opciones = [f"{p['id']}- {p['nombre']} - ${p['precio']:.2f} | Stock: {p['cantidad']}" for p in productos]
  opciones.append("Volver")

  current_row = 0
  while True:
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    # Título:
    titulo = "🆕 ELIMINAR PRODUCTO"
    separador = "─" * (len(titulo) + 4)
    stdscr.addstr(1, max(2, w//2 - len(titulo)//2), titulo)
    stdscr.addstr(2, max(2, w//2 - len(separador)//2), separador)
    stdscr.refresh()

    # Productos:
    for idx, row in enumerate(opciones):
      x = 2
      y = 3 + idx
      if idx == current_row:
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(y, x, row)
        stdscr.attroff(curses.color_pair(1))
      else:
         stdscr.addstr(y, x, row)
    stdscr.refresh()

    key = stdscr.getch()
    if key == curses.KEY_UP and current_row > 0:
       current_row -= 1
    elif key == curses.KEY_DOWN and current_row < len(opciones) - 1:
       current_row += 1
    elif key in [curses.KEY_ENTER, 10, 13]:
       if opciones[current_row] == "Volver":
          break
       producto = productos[current_row]
       stdscr.clear()
       msg = f"⚠ Eliminar '{producto['nombre']}'? (s/n)"
       stdscr.addstr(2, 2, msg)
       stdscr.refresh()
       confirmar = stdscr.getkey().lower()
       if confirmar == 's':
          cursor.execute("DELETE FROM productos WHERE id = ?", (producto['id'],))
          conn.commit()
          stdscr.addstr(4, 2, "✅ Producto eliminado correctamente.")
          stdscr.refresh()
          stdscr.getch()
          break
       
  conn.close()
