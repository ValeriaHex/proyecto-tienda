import sqlite3
from modelos.producto import Producto
from database.conexion import get_db_connection

class ProductoDao:
    def agregarP(self, producto: Producto):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
           "INSERT INTO productos (nombre, precio, talla, color, categoria, cantidad) VALUES (?, ?, ?, ?, ?, ?)", 
           (producto.nombre, producto.precio, producto.talla, producto.color, producto.categoria, producto.cantidad)
        )
        conn.commit()
        conn.close()

    def listarP(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, precio, talla, color, categoria, cantidad FROM productos")
        filas = cursor.fetchall()
        conn.close()

        productos = []
        for row in filas:
            try:
                precio = float(row["precio"])
            except ValueError:
                precio = 0.0
            try:
                cantidad = int(row["cantidad"])
            except (ValueError, TypeError):
                cantidad = 0
            productos.append(
                Producto(
                    nombre = row["nombre"],
                    precio = precio, 
                    talla = row["talla"],
                    color = row["color"],
                    categoria = row["categoria"],
                    cantidad = cantidad,
                    id = row["id"]
                )
            )
        return productos
    
    def actu_cantidad(self, producto: Producto):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE productos SET cantidad=? WHERE id=?", (producto.cantidad, producto.id))
        conn.commit()
    
    def eliminarP(self, id_prod):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_prod,))
        conn.commit()
        conn.close()

    