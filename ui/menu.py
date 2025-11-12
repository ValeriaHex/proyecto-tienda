import curses
from rich.console import Console

console = Console()
def main_menu(stdscr):
    curses.curs_set(0)

    menu = [
        "Gestionar productos",
        "Gestionar clientes",
        "Gestionar ventas",
        "Gestionar inventario",
        "Salir"
    ]
    current_row = 0

    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_MAGENTA)

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        #Mostrar menu
        for idx, row in enumerate(menu):
            x = w//2 - len(row)//2
            y = h//2 - len(menu)//2 + idx
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)
        
        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0 :
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            return menu[current_row]