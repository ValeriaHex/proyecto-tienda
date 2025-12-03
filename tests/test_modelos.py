import unittest
from modelos.producto import Producto
from modelos.cliente import Cliente
from modelos.venta import Venta
from datetime import datetime

class TestModelos(unittest.TestCase):

    def test_prod_attrs(self):
        p = Producto(
            nombre="Prueba", 
            precio=10.5, 
            talla="M", 
            color="Plateado", 
            categoria="Camisetas", 
            cantidad=5, 
            id=1
        )
        self.assertEqual(p.nombre, "Prueba")
        self.assertEqual(p.precio, 10.5)
        self.assertEqual(p.cantidad, 5)
        self.assertEqual(p.id, 1)
        self.assertIn("Prueba", str(p))

    def test_clien_attrs(self):
        c = Cliente("Ana Martinez", "anamrtnz@gmail.com", "Caro, Potosí")
        self.assertEqual(c.nombre, "Ana Martinez")
        self.assertEqual(c.correo, "anamrtnz@gmail.com")
        self.assertIn("Caro, Potosí", c.direccion)
        self.assertIsNotNone(c.fecha_registro)

    def test_venta_fecha(self):
        productos = [
            {"nombre": "X", "cantidad": 2, "precio_unitario": 5.0, "subtotal": 10.0},
            {"nombre": "Y", "cantidad": 1, "precio_unitario": 8.5, "subtotal": 8.5}
        ]
        v = Venta(productos)
        self.assertAlmostEqual(v.total, 18.5)
        self.assertIsNotNone(v.fecha)

if __name__ == "__main__":
    unittest.main()