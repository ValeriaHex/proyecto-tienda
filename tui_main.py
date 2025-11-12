import curses 
from ui.menu import main_menu
from rich.prompt import Prompt
from managers.producto_manager import agregar_productos, listar_productos, eliminar_producto
from managers.cliente_manager import agregar_clientes, listar_clientes, eliminar_cliente
from managers.venta_manager import registrar_venta, listar_ventas, eliminar_venta
from managers.inventario_manager import mostrar_inventario, actualizar_stock

def pausa():
    Prompt.ask("\n Presiona enter para continuar...")

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
        
def run_tui():
    while True:
        op = curses.wrapper(main_menu)

        if op == "Salir":
            break

        # PRODUCTOS:
        elif op == "Gestionar productos":
            sub_menu = ["Agregar producto", "Listar productos", "Eliminar producto", "Volver"]
            sub_op = curses.wrapper(lambda stdscr: select_submenu(stdscr, sub_menu))

            if sub_op == "Agregar producto":
                agregar_productos()
                pausa()
            elif sub_op == "Listar productos":
                listar_productos()
                pausa()
            elif sub_op == "Eliminar producto":
                eliminar_producto()
                pausa()

        # CLIENTES:
        elif op == "Gestionar clientes":
            sub_menu = ["Agregar cliente", "Listar clientes", "Eliminar cliente", "Volver"]
            sub_op = curses.wrapper(lambda stdscr: select_submenu(stdscr, sub_menu))

            if sub_op == "Agregar cliente":
                agregar_clientes()
                pausa()
            elif sub_op == "Listar clientes":
                listar_clientes()
                pausa()
            elif sub_op == "Eliminar cliente":
                eliminar_cliente()
                pausa()

         # VENTAS:
        elif op == "Gestionar ventas":
            sub_menu = ["Registrar venta", "Listar ventas", "Eliminar venta", "Volver"]
            sub_op = curses.wrapper(lambda stdscr: select_submenu(stdscr, sub_menu))

            if sub_op == "Registrar venta":
                registrar_venta()
                pausa()
            elif sub_op == "Listar ventas":
                listar_ventas()
                pausa()
            elif sub_op == "Eliminar venta":
                eliminar_venta()
                pausa()

        # INVENTARIO:
        elif op == "Gestionar inventario":
            sub_menu = ["Mostrar inventario", "Actualizar stock", "Volver"]
            sub_op = curses.wrapper(lambda stdscr: select_submenu(stdscr, sub_menu))

            if sub_op == "Mostrar inventario":
                mostrar_inventario()
                pausa()
            elif sub_op == "Actualizar stock":
                actualizar_stock()
                pausa()

if __name__ == "__main__":
    run_tui()
            