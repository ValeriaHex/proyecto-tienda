from database.conexion import get_db_connection, DB_PATH

def crear_tablas():
	conn = get_db_connection()
	cursor = conn.cursor()

	#Crear tabla productos
	cursor.execute("""
	  CREATE TABLE IF NOT EXISTS productos (
	    id INTEGER PRIMARY KEY AUTOINCREMENT,
	    nombre TEXT NOT NULL,
	    precio REAL NOT NULL DEFAULT 0.0,
	    talla TEXT,
	    color TEXT,
	    categoria TEXT,
	    cantidad INTEGER NOT NULL DEFAULT 0
	  )
	  """
	)

        #Crear tabla clientes
	cursor.execute("""
	  CREATE TABLE IF NOT EXISTS clientes (
	    id INTEGER PRIMARY KEY AUTOINCREMENT,
	    nombre TEXT NOT NULL,
	    correo TEXT,
	    direccion TEXT,
	    fecha_registro TEXT NOT NULL
	  )
	  """
	)

        #Crear tabla ventas
	cursor.execute("""
	  CREATE TABLE IF NOT EXISTS ventas (
	    id INTEGER PRIMARY KEY AUTOINCREMENT,
	    cliente_id INTEGER,
	    total REAL NOT NULL DEFAULT 0.0,
	    fecha TEXT NOT NULL,
	    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE SET NULL
	  )
	  """
	)

        #Crear tabla venta_items
	cursor.execute("""
	  CREATE TABLE IF NOT EXISTS venta_items (
	    id INTEGER PRIMARY KEY AUTOINCREMENT,
	    venta_id INTEGER NOT NULL,
	    producto_id INTEGER,
	    nombre TEXT NOT NULL,
	    cantidad INTEGER NOT NULL,
	    precio_unitario REAL NOT NULL,
	    subtotal REAL NOT NULL,
	    FOREIGN KEY (venta_id) REFERENCES ventas(id) ON DELETE CASCADE,
	    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE SET NULL
	  )
	  """
	)

	conn.commit()
	conn.close()
	print("✅ Tablas creadas correctamente (si no existían). Archivo DB: ", DB_PATH)

if __name__ == "__main__":
	crear_tablas()

