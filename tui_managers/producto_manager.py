import curses
from modelos.producto import Producto
from dao.productoDAO import ProductoDao
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
  
  producto = Producto(nombre, precio, talla, color,categoria, cantidad)
  dao = ProductoDao()
  dao.agregarP(producto)

  stdscr.addstr(8, 2, f"✅ Producto '{nombre}' agregado correctamente.")
  stdscr.refresh()
  stdscr.getch()

def listar_productos_tui(stdscr):
  dao = ProductoDao()
  productos = dao.listarP()
    
  if not productos:
    stdscr.clear()
    stdscr.addstr(2, 2, "⛔ No hay productos registrados.")
    stdscr.refresh()
    stdscr.getch()
    return

  stdscr.clear()
  stdscr.addstr(1, 2, "📋 LISTA DE PRODUCTOS")
  stdscr.addstr(2, 2, "──────────────────────────────────────────────────────────────────────────────")
  stdscr.addstr(3, 2, f" {'ID':<4} {'Nombre':<20} {'Precio':<10} {'Stock':<8} {'Talla':<8} {'Color':<10} {'Categoría'}")
  stdscr.addstr(4, 2, "──────────────────────────────────────────────────────────────────────────────")
  
  ult_fila = 4 + len(productos)
  for i, p in enumerate(productos):
    
    try:
      precio = float(p.precio)
      cantidad = int(p.cantidad)
    except (ValueError, TypeError):
      precio = 0.0
      cantidad = 0
      
    stdscr.addstr(5+i, 3, f"{p.id:<4} {p.nombre:<20} ${p.precio:<9.2f} {p.cantidad:<8} {p.talla or '-':<8} {p.color or '-':<10} {p.categoria or '-'}")  
    stdscr.addstr(ult_fila+1, 2, "──────────────────────────────────────────────────────────────────────────────")
  stdscr.refresh()
  stdscr.getch()

def eliminar_producto_tui(stdscr):
  curses.curs_set(0)
  dao = ProductoDao()
  productos = dao.listarP()
  
  if not productos:
    stdscr.clear()
    stdscr.addstr(2, 2, "⛔ No hay productos registrados.")
    stdscr.refresh()
    stdscr.getch() 
    return
  
  opciones = [f"{p.id}. {p.nombre} - ${p.precio:.2f} | Stock: {p.cantidad}" for p in productos]
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
       msg = f"⚠ Eliminar '{producto.nombre}'? (s/n)"
       stdscr.addstr(2, 2, msg)
       stdscr.refresh()
       confirmar = stdscr.getkey().lower()
       if confirmar == 's':
          dao.eliminarP(producto.id)
          stdscr.addstr(4, 2, "✅ Producto eliminado correctamente.")
          stdscr.refresh()
          stdscr.getch()
          break
       
