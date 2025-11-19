from datetime import datetime

class Cliente:

	def __init__(self, nombre, correo, direccion):
		self.nombre = nombre
		self.correo = correo
		self.direccion = direccion
		self.fecha_registro = datetime.now().strftime("%Y-%m-%d || %H:%M:%S")

	def __str__(self):
		return f"{self.nombre} - {self.correo} - {self.direccion} - {self.fecha_registro}"

