import curses

def main_menu(stdscr):
    curses.curs_set(0)

    options = [
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
        if key == curses.KEY_UP and current_row > 0 :
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(options) - 1:
            current_row += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            return options[current_row]