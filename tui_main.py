import curses 
from ui.menu import main_menu
from rich.prompt import Prompt
from contextlib import redirect_stdout
import io
from managers.producto_manager import listar_productos
from tui_managers.producto_manager import agregar_productos_tui, eliminar_producto_tui
from managers.cliente_manager import agregar_clientes, listar_clientes, eliminar_cliente
from managers.venta_manager import registrar_venta, listar_ventas, eliminar_venta
from managers.inventario_manager import mostrar_inventario, actualizar_stock

def pausa():
    Prompt.ask("\n Presiona enter para continuar...")

def mostrar_output_curses(stdscr, funcion, *args, **kwargs):
    h, w = stdscr.getmaxyx()
    win = curses.newwin(h-2, w-2, 1, 1)
    win.box()

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        funcion(*args, **kwargs)

    lines = buffer.getvalue().splitlines()
    for idx, line in enumerate(lines):
        if idx >= h-4:
            break
        win.addstr(idx+1, 1, line[:w-4])
    win.refresh()
    win.getch()

def select_submenu(stdscr, options):
    curses.curs_set(0)
    current_row = 0
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        for idx, row in enumerate(options):
            x = w//2 - len(row)//2
            y = h//2 - len(options)//2 + idx
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
        elif key == curses.KEY_DOWN and current_row < len(options) - 1:
            current_row += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            return options[current_row]
        
def run_tui(stdscr):
    while True:
        op = main_menu(stdscr)

        if op == "Salir":
            break

        # PRODUCTOS:
        elif op == "Gestionar productos":
            sub_menu = ["Agregar producto", "Listar productos", "Eliminar producto", "Volver"]
            sub_op = select_submenu(stdscr, sub_menu)

            if sub_op == "Agregar producto":
                agregar_productos_tui(stdscr)
            elif sub_op == "Listar productos":
                mostrar_output_curses(stdscr, listar_productos)
            elif sub_op == "Eliminar producto":
                eliminar_producto_tui(stdscr)

        # CLIENTES:
        elif op == "Gestionar clientes":
            sub_menu = ["Agregar cliente", "Listar clientes", "Eliminar cliente", "Volver"]
            sub_op = select_submenu(stdscr, sub_menu)

            if sub_op == "Agregar cliente":
                mostrar_output_curses(stdscr, agregar_clientes)
            elif sub_op == "Listar clientes":
                mostrar_output_curses(stdscr, listar_clientes)
            elif sub_op == "Eliminar cliente":
                mostrar_output_curses(stdscr, eliminar_cliente)

         # VENTAS:
        elif op == "Gestionar ventas":
            sub_menu = ["Registrar venta", "Listar ventas", "Eliminar venta", "Volver"]
            sub_op = select_submenu(stdscr, sub_menu)

            if sub_op == "Registrar venta":
                mostrar_output_curses(stdscr, registrar_venta)
            elif sub_op == "Listar ventas":
                mostrar_output_curses(stdscr, listar_ventas)
            elif sub_op == "Eliminar venta":
                mostrar_output_curses(stdscr, eliminar_venta)

        # INVENTARIO:
        elif op == "Gestionar inventario":
            sub_menu = ["Mostrar inventario", "Actualizar stock", "Volver"]
            sub_op = select_submenu(stdscr, sub_menu)

            if sub_op == "Mostrar inventario":
                mostrar_output_curses(stdscr, mostrar_inventario)
            elif sub_op == "Actualizar stock":
                mostrar_output_curses(stdscr, actualizar_stock)

if __name__ == "__main__":
    curses.wrapper(run_tui)
            