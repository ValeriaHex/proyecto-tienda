import unittest
from tests.test_utils import crear_db_temporal, borrar_db
from dao.productoDAO import ProductoDao
from modelos.producto import Producto

class testProductoDAO(unittest.TestCase):

    def setUp(self):
        self.db_path = crear_db_temporal()
        self.dao = ProductoDao()

    def tearDown(self):
        borrar_db(self.db_path)

    def test_agregar_listar(self):
        p = Producto("Camisa", 30.0, "L", "Rosa", "Camisetas", 10)
        self.dao.agregarP(p)
        productos = self.dao.listarP()
        self.assertTrue(any(prod.nombre == "Camisa" for prod in productos))

    def test_actucantidad(self):
        p = Producto("Pantalón", 40.0, "M", "Negro", "Pantalones", 5)
        self.dao.agregarP(p)
        productos = self.dao.listarP()
        prod = productos[0]
        prod.cantidad = 2
        try:
            self.dao.actu_cantidad(prod)
        except TypeError:
            self.dao.actu_cantidad(prod.id, prod.cantidad)
            productos2 = self.dao.listarP()
            self.assertEqual(productos2[0].cantidad, 2)

    def test_eliminar(self):
        p = Producto("EliminarTest", 5.0, "", "", "", 1)
        self.dao.agregarP(p)
        productos = self.dao.listarP()
        pid = productos[0].id
        self.dao.eliminarP(pid)
        productos2 = self.dao.listarP()
        self.assertFalse(any(prod.id == pid for prod in productos2))

if __name__ == "__main__":
    unittest.main()
