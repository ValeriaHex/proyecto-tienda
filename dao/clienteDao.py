import sqlite3
from modelos.cliente import Cliente
from database.conexion import get_db_connection

class ClienteDAO:

    def agregarC(self, cliente: Cliente):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clientes (nombre, correo, direccion, fecha_registro) VALUES (?, ?, ?, ?)",
            (cliente.nombre, cliente.correo, cliente.direccion, cliente.fecha_registro)
        )
        conn.commit()
        conn.close()

    def listarC(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")
        filas = cursor.fetchall()
        conn.close()

        clientes =[]
        for row in filas:
            clientes.append(
                Cliente(
                    nombre = row['nombre'],
                    correo = row['correo'],
                    direccion = row['direccion']
                )
            )
            clientes[-1].id = row['id']
            clientes[-1].fecha_registro = row['fecha_registro']
        return clientes
    
    def eliminarC(self, id_cli):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cli,))
        conn.commit()
        conn.close()