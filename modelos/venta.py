from datetime import datetime

class Venta:

	def __init__(self,productos_comprados):
	  self.productos = productos_comprados
	  self.total = sum(item['subtotal'] for item in productos_comprados)
	  self.fecha = datetime.now().strftime("%Y-%m-%d || %H:%M:%S")

