import unittest
from tests.test_utils import crear_db_temporal, borrar_db
from dao.productoDAO import ProductoDao
from dao.ventaDAO import VentaDAO
from modelos.producto import Producto
from modelos.venta import Venta

class TestVentaDAO(unittest.TestCase):

    def setUp(self):
        self.db_path = crear_db_temporal()
        self.prod_dao = ProductoDao()
        self.venta_dao = VentaDAO()

    def tearDown(self):
        borrar_db(self.db_path)

    def test_registrar_listar(self):
        p = Producto("Venta1", 20.0, "M", "Azul", "CamisetasV", 10)
        self.prod_dao.agregarP(p)
        productos = self.prod_dao.listarP()
        
        prod = productos[0]
        carrito = [{"producto_id": prod.id, "nombre": prod.nombre, "cantidad": 2, "precio_unitario": prod.precio, "subtotal": prod.precio * 2}]
        venta = Venta(carrito)
        vid = self.venta_dao.agregarV(venta)
        ventas = self.venta_dao.listarV()
        self.assertTrue(any(v.id == vid for v in ventas))

    def test_eliminar_venta(self):
        p = Producto("Venta2", 10.0, "S", "", "", 5)
        self.prod_dao.agregarP(p)
        prod = self.prod_dao.listarP()[0]
        carrito = [{"producto_id": prod.id, "nombre": prod.nombre, "cantidad": 1, "precio_unitario": prod.precio, "subtotal": prod.precio}]
        venta = Venta(carrito)
        vid = self.venta_dao.agregarV(venta)
        self.venta_dao.eliminarV(vid)
        ventas = self.venta_dao.listarV()
        self.assertFalse(any(v.id == vid for v in ventas))

if __name__ == "__main__":
    unittest.main()