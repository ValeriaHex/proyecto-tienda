from modelos.venta import Venta
from database.conexion import get_db_connection
from datetime import datetime

ventas = []
def registrar_venta():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos")
    filas = cursor.fetchall()
    productos = [dict(prod) for prod in filas]
    
    if len(productos) == 0:
        print(" ⛔ No hay productos disponibles para vender.")
        conn.close()
        return

    carrito = [] #productos comprados en esta venta
    while True:
        print("\n 🛒 Productos Disponibles")
        print("────────────────────────────────────────────────")
        print(f" {'N°':<4} {'Producto':<23} {'Precio':<10} {'Stock'}")
        print("────────────────────────────────────────────────")

        for i, prod in enumerate(productos):
            #print(f" {i+1}. {prod['nombre']} - ${prod['precio']} - Stock: {prod['cantidad']}")
            print(f" {i+1:<4} {prod['nombre']:<23} ${prod['precio']:<9.2f} {prod['cantidad']}")
        print("────────────────────────────────────────────────")

        elec = input(" ❣ Elige el número del producto (o 0 para terminar): ")

        if elec == "0":
            break

        try:
            indice = int(elec) - 1
            if indice < 0 or indice >= len(productos):
                print(" ⚠ Opción inválida.")
                continue
            
            producto = productos[indice]

            #verificar stock
            cantidad = int(input(f" 📦 Cantidad de '{producto['nombre']}': "))
            if cantidad > producto['cantidad']:
                print(" ⚠ No hay suficiente stock.")
                continue

            #Calcular subtotal
            subtotal = producto['precio'] * cantidad

            #Guardar en el carrito
            carrito.append({"nombre": producto['nombre'], "cantidad": cantidad, "precio_unitario": producto['precio'], "subtotal": subtotal})

            #Actualizar stock del producto
            nueva_cantidad = producto['cantidad'] - cantidad
            cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nueva_cantidad, producto['id']))
            conn.commit()

            productos[indice]['cantidad'] = nueva_cantidad

            print(f" ✅ Agregado: {cantidad} x {producto['nombre']} (${subtotal:.2f})")

        except ValueError:
            print(" ⚠ Se debe ingresar un número válido.")

    if len(carrito) == 0:
        print(" ⛔ No se registró ninguna venta.")
        conn.close()
        return

    #venta = Venta(carrito)
    #ventas.append(venta)

    # Calcular total
    total_venta = sum(item['subtotal'] for item in carrito)
    fecha_actual = datetime.now().strftime('%Y-%m-%d || %H:%M:%S')

    # Insertar venta
    cursor.execute("INSERT INTO ventas (cliente_id, total, fecha) VALUES (?, ?, ?)", (None, total_venta, fecha_actual))
    venta_id = cursor.lastrowid

    # Insertar detalles de la venta
    for item in carrito:
        producto_id = next((p['id'] for p in productos if p['nombre'] == item['nombre']), None)
        cursor.execute("""
            INSERT INTO venta_items (venta_id, producto_id, nombre, cantidad, precio_unitario, subtotal) VALUES (?, ?, ?, ?, ?, ?)
            """, (venta_id, producto_id, item['nombre'], item['cantidad'], item['precio_unitario'], item['subtotal']))
    
    conn.commit()

    print("\n ✅ ¡Venta registrada con éxito!\n")
    print(" 🧾 Detalles de la venta")
    print("─────────────────────────────────────────")
    for item in carrito:
        print(f" 🛍️ {item['cantidad']} x {item['nombre']} @ ${item['precio_unitario']:.2f} = ${item['subtotal']:.2f}")
    print("─────────────────────────────────────────")
    print(f" 💵 Total de la venta: ${total_venta:.2f}")
    conn.close()

def listar_ventas():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ventas ORDER BY fecha DESC")
    ventas = cursor.fetchall()

    if not ventas:
        print(" ⛔ No hay ventas registradas.")
        conn.close()
        return

    print("\n 📒 Historial de Ventas")
    print("═════════════════════════════════════════════════════════════════")
    for v in ventas:
        print(f"\n 🧾 Venta ID: {v['id']} | Fecha: {v['fecha']} | Total: ${v['total']:.2f}")
        print("   Detalles:")
        cursor.execute("SELECT * FROM venta_items WHERE venta_id = ?", (v['id'],))
        items = cursor.fetchall()

        for item in items:
            #print(f" {item['cantidad']} x {item['nombre']} -> ${item['precio_unitario']} = ${item['subtotal']}")
             print(f"   • {item['cantidad']} x {item['nombre']} -> ${item['precio_unitario']:.2f} = ${item['subtotal']:.2f} \n")
        
    print("═════════════════════════════════════════════════════════════════\n")
    
    conn.close()

