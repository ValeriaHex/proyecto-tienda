import unittest
from tests.test_utils import crear_db_temporal, borrar_db
from dao.inventarioDAO import InventarioDAO
from dao.productoDAO import ProductoDao
from modelos.producto import Producto

class TestInventarioDAO(unittest.TestCase):

    def setUp(self):
        self.db_path = crear_db_temporal()
        self.dao_i = InventarioDAO()
        self.prod_dao = ProductoDao()

    def tearDown(self):
        borrar_db(self.db_path)

    def test_mostrar_y_actualizar(self):
        p = Producto("tInventario", 12.0, "", "", "", 7)
        self.prod_dao.agregarP(p)
        productos = self.dao_i.mostrarI()
        self.assertTrue(len(productos) > 0)
        prod = productos[0]
        try:
            self.dao_i.actualizarS(prod.id, 3)
        except TypeError:
            prod.cantidad = 3
            self.dao_i.actualizarS(prod)
        productos2 = self.dao_i.mostrarI()
        self.assertEqual(productos2[0].cantidad, 3)

if __name__ == "__main__":
    unittest.main()