import curses
from modelos.cliente import Cliente
from database.conexion import get_db_connection
from datetime import datetime
from curses import textpad

def input_box(stdscr, prompt):
  curses.curs_set(1)
  stdscr.clear()
  h, w = stdscr.getmaxyx()

  titulo = "🆕 REGISTRAR NUEVO CLIENTE"
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

def agregar_clientes_tui(stdscr):
	stdscr.clear()
	h, w = stdscr.getmaxyx()

	nombre = input_box(stdscr, "🔤 Nombre del cliente: ")
	correo = input_box(stdscr, "📧 Correo del cliente: ")
	direccion = input_box(stdscr, "🏠 Direccion de envío: ")

	cliente = Cliente(nombre, correo, direccion)
	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute(
	  "INSERT INTO clientes (nombre, correo, direccion, fecha_registro) VALUES (?, ?, ?, ?)",
	  (cliente.nombre, cliente.correo, cliente.direccion, cliente.fecha_registro)
	)
	conn.commit()
	conn.close()

	stdscr.addstr(8, 2, f"✅ Cliente '{nombre}' agregado correctamente.")
	stdscr.refresh()
	stdscr.getch()

def listar_clientes():
	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM clientes")
	filas = cursor.fetchall()
	conn.close()

	if not filas:
		print(" ⛔ No hay clientes registrados.")
		return
	print("\n 📋 LISTA DE CLIENTES ")
	print("───────────────────────────────────────────────────────────────────────────────────────────────")
	print(f" {'ID':<3} {'Nombre':<15} {'Correo':<20} {'Dirección':<25} {'Fecha Registro'}")
	print("───────────────────────────────────────────────────────────────────────────────────────────────")

	#for i, fila in enumerate(filas, 1):
	#	print(f" {i}. {fila['nombre']} - {fila['correo']} - {fila['direccion']} - {fila['fecha_registro']}")
	for fila in filas:
		print(f" {fila['id']:<3} {fila['nombre']:<15} {fila['correo']:<20} {fila['direccion']:<25} {fila['fecha_registro']}")

	print("───────────────────────────────────────────────────────────────────────────────────────────────\n")

def eliminar_cliente_tui(stdscr):
  curses.curs_set(0)
  conn = get_db_connection()
  cursor = conn.cursor()
  
  cursor.execute("SELECT id, nombre, correo, direccion FROM clientes ORDER BY id")
  clientes = cursor.fetchall()
  
  if not clientes:
    stdscr.clear()
    stdscr.addstr(2, 2, "⛔ No hay clientes registrados.")
    stdscr.refresh()
    stdscr.getch()
    conn.close()
    return
  
  opciones = [f"{p['id']}- {p['nombre']}  | Correo: {p['correo']}" for p in clientes]
  opciones.append("Volver")

  current_row = 0
  while True:
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    # Título:
    titulo = "🆕 ELIMINAR CLIENTE"
    separador = "─" * (len(titulo) + 4)
    stdscr.addstr(1, max(2, w//2 - len(titulo)//2), titulo)
    stdscr.addstr(2, max(2, w//2 - len(separador)//2), separador)
    stdscr.refresh()

    # Clientes:
    for idx, row in enumerate(opciones):
      x = 2
      y = 4 + idx
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
       cliente = clientes[current_row]
       stdscr.clear()
       msg = f"⚠ Eliminar cliente '{cliente['nombre']}'? (s/n)"
       stdscr.addstr(2, 2, msg)
       stdscr.refresh()
       confirmar = stdscr.getkey().lower()
       
       if confirmar == 's':
          cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente['id'],))
          conn.commit()
          stdscr.addstr(4, 2, "✅ Cliente eliminado correctamente.")
          stdscr.refresh()
          stdscr.getch()
          break
       
  conn.close()