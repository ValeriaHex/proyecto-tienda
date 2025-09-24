from modelos.cliente import Cliente

clientes = []

def agregar_clientes():
	nombre = input(" Nombre del cliente: ")
	correo = input(" Correo del cliente: ")
	direccion = input(" Dirrecion de envío: ")

	cliente = Cliente(nombre, correo, direccion)
	clientes.append(cliente)
	print(f" Cliente '{nombre}' agregado correctamente.")

def listar_clientes():
	if not clientes:
		print(" No hay clientes registrados.")
		return
	print("\n -------- Lista de clientes --------")
	for i, c in enumerate(clientes, 1):
		print(f" {i}.  {c}")



