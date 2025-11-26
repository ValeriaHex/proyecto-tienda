import sqlite3
from modelos.producto import Producto
from database.conexion import get_db_connection

class InventarioDAO:
    
    def mostrarI(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
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
    
    def actualizarS(self, producto_id, ncant):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (ncant, producto_id))
        conn.commit()
        conn.close()