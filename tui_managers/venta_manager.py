import curses
from modelos.venta import Venta
from dao.ventaDAO import VentaDAO
from dao.productoDAO import ProductoDao
from datetime import datetime
from curses import textpad

def input_box(stdscr, prompt, y_start):
    curses.curs_set(1)
    h, w = stdscr.getmaxyx()
    stdscr.addstr(y_start, 2, prompt[:w-4])
    stdscr.refresh()

    win = curses.newwin(3, w-4, y_start+1, 2)
    win.box()
    win.refresh()

    curses.echo()
    ui = win.getstr(1, 1, w-6).decode("utf-8")
    curses.noecho()
    return ui

def registrar_venta_tui(stdscr):
    curses.curs_set(0)
    daop = ProductoDao()
    productos = daop.listarP()
    
    if not productos:
        stdscr.addstr(2, 2,"⛔ No hay productos disponibles para vender.")
        stdscr.refresh()
        stdscr.getch()
        return

    carrito = []
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Título
        titulo = "🛒 REGISTRAR NUEVA VENTA"
        separador = "─" * (len(titulo)+4)
        stdscr.addstr(1, max(2, w//2 - len(titulo)//2), titulo)
        stdscr.addstr(2, max(2, w//2 - len(separador)//2), separador)

        # Lista de productos
        stdscr.addstr(3, 2, f"{'N°':<4} {'Producto':<20} {'Precio':<10} {'Stock'}")
        stdscr.addstr(4, 2, "─"*44)
        for i, p in enumerate(productos):
            stdscr.addstr(5+i, 2, f"{i+1:<4} {p.nombre:<20} ${p.precio:<9.2f} {p.cantidad}")

        stdscr.refresh()

        elec = input_box(stdscr, "Elige número del producto (0 para terminar):", y_start=6+len(productos))
        if elec == "0":
            break

        try:
            indice = int(elec) - 1
            if indice < 0 or indice >= len(productos):
                raise ValueError

            producto = productos[indice]

            cantidad_str = input_box(stdscr, f"Cantidad de '{producto.nombre}':", y_start=11+len(productos))
            cantidad = int(cantidad_str)

            if cantidad > producto.cantidad:
                stdscr.addstr(15+len(productos), 2, "⚠ No hay suficiente stock.")
                stdscr.refresh()
                stdscr.getch()
                continue

            subtotal = producto.precio * cantidad
            carrito.append({"producto_id": producto.id, "nombre": producto.nombre, "cantidad": cantidad, "precio_unitario": producto.precio, "subtotal": subtotal})
            producto.cantidad -= cantidad
            daop = ProductoDao()
            daop.actu_cantidad(producto)
            productos[indice].cantidad = producto.cantidad

            stdscr.addstr(15+len(productos), 2, f"✅ Agregado: {cantidad} x {producto.nombre} (${subtotal:.2f})")
            stdscr.refresh()
            stdscr.getch()

        except ValueError:
            stdscr.addstr(13+len(productos), 2, "⚠ Debes ingresar un número válido")
            stdscr.refresh()
            stdscr.getch()

    if carrito:
        venta = Venta(productos_comp=carrito)
        daov = VentaDAO()
        daov.agregarV(venta)
        
        stdscr.addstr(12+len(productos), 2, f"✅ Venta registrada con éxito! Total: ${venta.total:.2f}")
        stdscr.refresh()
        stdscr.getch()

    else:
        stdscr.addstr(12+len(productos), 2, f"⚠ No se registro ninguna venta.")
        stdscr.refresh()
        stdscr.getch()

def listar_ventas_tui(stdscr): 
    dao = VentaDAO()
    ventas = dao.listarV()

    if not ventas:
        stdscr.clear()
        stdscr.addstr(2, 2, "⛔ No hay ventas registradas.")
        stdscr.refresh()
        stdscr.getch()
        return

    stdscr.clear()
    stdscr.addstr(1, 2, "📒 HISTORIAL DE VENTAS")
    stdscr.addstr(2, 2, "──────────────────────────────────────────────────────────────────")
    fila = 3
    for v in ventas:
        stdscr.addstr(fila, 2, f"🧾 Venta ID: {v.id} | Fecha: {v.fecha} | Total: ${v.total:.2f}")
        fila += 1
        stdscr.addstr(fila, 4, "   Detalles:")
        fila += 1
        for item in v.productos:
             stdscr.addstr(fila, 6, f"   • {item['cantidad']} x {item['nombre']} -> ${item['precio_unitario']:.2f} = ${item['subtotal']:.2f}")
             fila += 1
        stdscr.addstr(fila, 2, "──────────────────────────────────────────────────────────────────")
    stdscr.refresh()
    stdscr.getch()

def eliminar_venta_tui(stdscr):
    curses.curs_set(0)
    dao = VentaDAO()
    ventas = dao.listarV()

    if not ventas:
        stdscr.clear()
        stdscr.addstr(2, 2, "⛔ No hay ventas registrados.")
        stdscr.refresh()
        stdscr.getch()
        return
    
    opciones = [f"{p.id}- {p.fecha} -> ${p.total:.2f}" for p in ventas]
    opciones.append("Volver")

    current_row = 0
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Título:
        titulo = "🆕 ELIMINAR VENTA"
        separador = "─" * (len(titulo) + 4)
        stdscr.addstr(1, max(2, w//2 - len(titulo)//2), titulo)
        stdscr.addstr(2, max(2, w//2 - len(separador)//2), separador)
        stdscr.refresh()

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
            venta_selec = ventas[current_row]
            stdscr.clear()
            msg = f"⚠ Eliminar venta ID'{venta_selec.id}'? (s/n)"
            stdscr.addstr(2, 2, msg)
            stdscr.refresh()
            confirmar = stdscr.getkey().lower()
            if confirmar == 's':
                dao.eliminarV(venta_selec.id)
                stdscr.addstr(4, 2, "✅ Venta eliminada correctamente.")
                stdscr.refresh()
                stdscr.getch()
                break
            else:
                stdscr.addstr(4, 2, "❌ Operación cancelada.")
                stdscr.refresh()
                stdscr.getch()
                break

