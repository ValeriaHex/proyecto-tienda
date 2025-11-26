import sqlite3
from modelos.venta import Venta
from database.conexion import get_db_connection

class VentaDAO:

    def agregarV(self, venta: Venta):  
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ventas (cliente_id, total, fecha) VALUES (?, ?, ?)", (None, venta.total, venta.fecha))
        venta_id = cursor.lastrowid

        for item in venta.productos:
            cursor.execute("""
                INSERT INTO venta_items (venta_id, producto_id, nombre, cantidad, precio_unitario, subtotal) VALUES (?, ?, ?, ?, ?, ?)""",
                (venta_id, item.get('producto_id'), item['nombre'], item['cantidad'], item['precio_unitario'], item['subtotal'])
            )
        conn.commit()
        conn.close()
        return venta_id
    
    def listarV(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ventas ORDER BY fecha ")
        filas = cursor.fetchall()

        ventas = []
        for v in filas:
            cursor.execute("SELECT * FROM venta_items WHERE venta_id = ?", (v['id'],))
            items = cursor.fetchall()
            productos = []
            for it in items:
                productos.append(
                    {
                        "producto_id": it['producto_id'],
                        "nombre": it['nombre'],
                        "cantidad": it['cantidad'],
                        "precio_unitario": it['precio_unitario'],
                        "subtotal": it['subtotal']
                    }
                )
            venta = Venta(
                productos_comp = productos,
                fecha = v['fecha'],              
                id = v['id']
            )
            ventas.append(venta)
        conn.close()
        return ventas
    
    def eliminarV(self, id_venta):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ventas WHERE id = ?", (id_venta,))
        conn.commit()
        conn.close()
