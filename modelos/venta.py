from datetime import datetime

class Venta:
	def __init__(self, productos_comp=None, total=None, fecha=None, id=None):
		self.id = id
		self.productos = productos_comp if productos_comp else []
		self.total = total if total is not None else sum(item['subtotal'] for item in self.productos)
		self.fecha = fecha if fecha else datetime.now().strftime("%Y-%m-%d || %H:%M:%S")

	def __str__(self):
		return f"Venta ID: {self.id} | Total: ${self.total:.2f} | Fecha: {self.fecha}"


