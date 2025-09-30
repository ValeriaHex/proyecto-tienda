class Producto:

	def __init__(self, nombre, precio, talla, color, categoria, cantidad):
	  self.nombre = nombre
	  self.precio = precio
	  self.talla = talla
	  self.color = color
	  self.categoria = categoria
	  self.cantidad = cantidad

	def __str__(self):
	  return f" {self.nombre} | Precio: ${self.precio} | Stock: {self.cantidad}"

