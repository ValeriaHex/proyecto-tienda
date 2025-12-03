import unittest
from tests.test_utils import crear_db_temporal, borrar_db
from dao.clienteDao import ClienteDAO
from modelos.cliente import Cliente

class testClienteDAO(unittest.TestCase):

    def setUp(self):
        self.db_path = crear_db_temporal()
        self.dao = ClienteDAO()

    def tearDown(self):
        borrar_db(self.db_path)

    def test_agregar_listar_eliminar(self):
        c = Cliente("Matteo Balsano", "matteoblsn@gmail.com", "Junin, Pagador")
        self.dao.agregarC(c)
        clientes = self.dao.listarC()
        self.assertTrue(any(cli.nombre == "Matteo Balsano" for cli in clientes))
        cid = clientes[0].id
        self.dao.eliminarC(cid)
        clientes2 = self.dao.listarC()
        self.assertFalse(any(cli.id == cid for cli in clientes2))

if __name__ == "__main__":
    unittest.main()