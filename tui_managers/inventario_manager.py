import curses
from dao.inventarioDAO import InventarioDAO
from curses import textpad

def input_box(stdscr, prompt, y_start):
    curses.curs_set(1)
    h, w = stdscr.getmaxyx()
    
    texto = prompt[:w-4]
    stdscr.addstr(y_start, 2, texto)
    stdscr.refresh()

    win = curses.newwin(3, w-4, y_start+1, 2)
    win.box()
    win.refresh()

    curses.echo()
    ui = win.getstr(1, 1, w-6).decode("utf-8")
    curses.noecho()
    curses.curs_set(0)
    return ui

def mostrar_inventario_tui(stdscr):
    stdscr.clear()
    dao = InventarioDAO()
    productos = dao.mostrarI()
    
    if not productos:   
        stdscr.clear()
        stdscr.addstr(2, 2, "⛔ No hay productos en el inventario.")
        stdscr.refresh()
        stdscr.getch()
        return
    
    stdscr.clear()
    stdscr.addstr(1, 2, "📦 INVENTARIO DE PRODUCTOS")
    stdscr.addstr(2, 2, "─────────────────────────────────────────────────────────────────────────────")
    stdscr.addstr(3, 2, f" {'ID':<4} {'Nombre':<20} {'Precio':<10} {'Stock':<7} {'Talla':<8} {'Color':<10} {'Categoría'}")
    stdscr.addstr(4, 2, "─────────────────────────────────────────────────────────────────────────────")

    ult_fila = 4 + len(productos)
    for i, p in enumerate(productos):
        try:
            precio = float(p.precio)
            cantidad = int(p.cantidad)
        except (ValueError, TypeError):
             precio = 0.0
             cantidad = 0
        stdscr.addstr(5+i, 3, f"{p.id:<4} {p.nombre:<20} ${p.precio:<9.2f} {p.cantidad:<7} {p.talla or '-':<8} {p.color or '-':<10} {p.categoria or '-'}")  
        stdscr.addstr(ult_fila+1, 2, "─────────────────────────────────────────────────────────────────────────────")
    stdscr.refresh()
    stdscr.getch()

def actualizar_stock_tui(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    dao = InventarioDAO()
    productos = dao.mostrarI()

    if not productos:
        stdscr.addstr(2, 2, "⛔ No hay productos para actualizar.")
        stdscr.refresh()
        stdscr.getch()
        return

	# Titulo:
    titulo = "🔧 ACTUALIZAR STOCK"
    separador = "─" * (len(titulo) + 4)
    h, w = stdscr.getmaxyx()
    stdscr.addstr(1, max(2, w//2 - len(titulo)//2), titulo)
    stdscr.addstr(2, max(2, w//2 - len(separador)//2), separador)

    # Listar productos:
    stdscr.addstr(3, 2, f"{'N°':<4} {'Producto':<20} {'Precio':<10} {'Stock'}")
    stdscr.addstr(4, 2, "─" * 44)

    for i, p in enumerate(productos):
        stdscr.addstr(5+i, 2, f"{i+1:<4} {p.nombre:<20} ${p.precio:<9.2f} {p.cantidad}")
    stdscr.refresh()
    
    # Elegir:
    op_str = input_box(stdscr, "❣ Elige el número del producto:", y_start=6+len(productos))

    try:
        op = int(op_str) - 1
        if op < 0 or op >= len(productos):
            stdscr.addstr(11+len(productos), 2, "⚠ Opción inválida.")
            stdscr.refresh()
            stdscr.getch()
            return

        selec = productos[op]
        prompt = f"📦 Nuevo stock para '{selec.nombre}': "
        nuevo_stock_str = input_box(stdscr, prompt, y_start=11+len(productos))
        nuevo_stock = int(nuevo_stock_str)

        dao.actualizarS(selec.id, nuevo_stock)

        stdscr.addstr(15+len(productos), 2, "✅ ¡Stock actualizado con éxito!")
        stdscr.refresh()
        stdscr.getch()

    except ValueError:
        stdscr.addstr(11+len(productos), 2, "⚠ Debes ingresar un número válido.")
        stdscr.refresh()
        stdscr.getch()

