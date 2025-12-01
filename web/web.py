import streamlit as st
from dao.productoDAO import ProductoDao
from dao.ventaDAO import VentaDAO
from dao.inventarioDAO import InventarioDAO
from dao.clienteDao import ClienteDAO
from modelos.producto import Producto
from modelos.cliente import Cliente
from modelos.venta import Venta

import streamlit as st

#Portada:
if "entrar" not in st.session_state:
    st.session_state.entrar = False

if not st.session_state.entrar:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown(
        """
        <h1 style='text-align: center; font-size: 48px; font-weight: 600;'>
            🛍️ GESTIÓN DE TIENDA
        </h1>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <p style='text-align: center; font-size: 20px; color: #555;'>
            Administra productos, clientes, ventas e inventario<br>
            de forma simple, clara y eficiente.
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("Ingresar", use_container_width=True):
            st.session_state.entrar = True
    st.stop()

# Titulo principal:
st.set_page_config(page_title="GESTIÓN DE TIENDA", page_icon="🛒")
st.title("🛒 GESTIÓN DE TIENDA")

#Pestañas:
menu = ["Gestionar productos", "Gestionar clientes", "Gestionar ventas", "Gestionar inventario"]
choice = st.sidebar.selectbox("Menú", menu)

#Productos:
if choice == "Gestionar productos":
    st.header("📦 Gestión de Productos")
    dao = ProductoDao()

    sub_menu = st.radio("Acción", ["Agregar", "Listar", "Eliminar"])

    if sub_menu == "Agregar":
        nombre = st.text_input("🔤 Nombre")
        precio = st.number_input("💲 Precio", min_value=0.0, step=0.5)
        talla = st.text_input("📏 Talla")
        color = st.text_input("🎨 Color")
        categoria = st.text_input("📂 Categoria")
        cantidad = st.number_input("📦 Cantidad", min_value=0, step=1)
        if st.button("Agregar Producto"):
            producto = Producto(nombre, precio, talla, color, categoria, cantidad)
            dao.agregarP(producto)
            st.success(f"✅ Producto '{nombre}' agregado correctamente.")
    
    elif sub_menu == "Listar":
        productos = dao.listarP()
        if not productos:
            st.warning("⛔ No hay productos registrados.")
        else:
            st.subheader("📋 Lista de productos")
            data = []
            for p in productos:
                data.append({
                    "ID": p.id,
                    "Nombre": p.nombre,
                    "Precio": f"$ {p.precio:.2f}",
                    "Talla": p.talla or "-",
                    "Color": p.color or "-",
                    "Categoría": p.categoria or "-",
                    "Cantidad": p.cantidad
                })
            st.dataframe(data)

    elif sub_menu == "Eliminar":
        productos = dao.listarP()
        for p in productos:
            if st.button(f"Eliminar producto {p.nombre}"):
                dao.eliminarP(p.id)
                st.success(f"✅ Producto '{p.nombre}' eliminado correctamente.")

#Clientes:
elif choice == "Gestionar clientes":
    st.header("👤 Gestión de Clientes")
    dao = ClienteDAO()

    sub_menu = st.radio("Acción", ["Agregar", "Listar", "Eliminar"])

    if sub_menu == "Agregar":
        nombre = st.text_input("🔤 Nombre")
        correo = st.text_input("📧 Correo")
        direccion = st.text_input("🏠 Direccion")
        if st.button("Agregar Cliente"):
            cliente = Cliente(nombre, correo, direccion)
            dao.agregarC(cliente)
            st.success(f"✅ Cliente '{nombre}' agregado correctamente.")
    
    elif sub_menu == "Listar":
        clientes = dao.listarC()
        if not clientes:
            st.warning("⛔ No hay clientes registrados.")
        else:
            st.subheader("📋 Lista de clientes")
            data = []
            for p in clientes:
                data.append({
                    "ID": p.id,
                    "Nombre": p.nombre,
                    "Correo": p.correo,
                    "Dirección": p.direccion,
                    "Fecha de registro": p.fecha_registro
                })
            st.dataframe(data)

    elif sub_menu == "Eliminar":
        clientes = dao.listarC()
        for p in clientes:
            if st.button(f"Eliminar cliente {p.nombre}"):
                dao.eliminarC(p.id)
                st.success(f"✅ Cliente '{p.nombre}' eliminado correctamente.")

#Ventas:
elif choice == "Gestionar ventas":
    st.header("💵 Gestión de Ventas")
    daop = ProductoDao()
    daov = VentaDAO()

    sub_menu = st.radio("Acción", ["Registrar", "Listar", "Eliminar"])

    if sub_menu == "Registrar":
        productos = daop.listarP()

        if not productos:
            st.warning("⛔ No hay productos disponibles para vender.")
        else:
            carrito = []
            for p in productos:
                cantidad = st.number_input(f"**{p.nombre}** | Precio: $ {p.precio:.2f} (Stock: {p.cantidad})", min_value=0, max_value=p.cantidad, step=1)
                if cantidad > 0:
                    subtotal = p.precio * cantidad
                    carrito.append({"producto_id": p.id, "nombre": p.nombre, "cantidad": cantidad, "precio_unitario": p.precio, "subtotal": subtotal})
            
            if st.button("Registrar Venta") and carrito:
                venta = Venta(productos_comp=carrito)
                daov.agregarV(venta)
                for item in carrito:
                    for prod in productos:
                        if prod.id == item["producto_id"]:
                            prod.cantidad -= item["cantidad"]
                            daop.actu_cantidad(prod)
                            break
                st.success(f"✅ Venta registrada! Total: $ {venta.total:.2f}")

    elif sub_menu == "Listar":
        ventas = daov.listarV()
        if not ventas:
            st.warning("⛔ No hay ventas registradas.")
        else:
            st.subheader("📒 Historial de ventas")
            for v in ventas:
                st.markdown(f"**🧾 Venta ID:** {v.id} | **Fecha:** {v.fecha} | **Total:** ${v.total:.2f}")
                st.markdown("**Detalles:**")
                data = []
                for item in v.productos:
                    data.append({
                        "Producto": item["nombre"],
                        "Cantidad": item["cantidad"],
                        "Precio Unitario": f"$ {item['precio_unitario']:.2f}",
                        "Subtotal": f"$ {item['subtotal']:.2f}"
                    })
                st.dataframe(data)
                st.markdown("---")

    elif sub_menu == "Eliminar":
        ventas = daov.listarV()
        if not ventas:
            st.warning("⛔ No hay ventas registradas.")
        else:
            for p in ventas:
                if st.button(f"Eliminar venta {p.id} -> Total: ${p.total:.2f}"):
                    daov.eliminarV(p.id)
                    st.success(f"✅ Venta '{p.id}' eliminada correctamente.")

#Inventario:
elif choice == "Gestionar inventario":
    st.header("📝 Gestión de Inventario")
    dao = InventarioDAO()
    productos = dao.mostrarI()

    sub_menu = st.radio("Acción", ["Mostrar inventario", "Actualizar stock"])

    if sub_menu == "Mostrar inventario":
        if not productos:
            st.warning("⛔ No hay productos para mostrar.")
        else:
            st.subheader("📋 Lista de productos")
            data = []
            for p in productos:
                data.append({
                    "ID": p.id,
                    "Nombre": p.nombre,
                    "Precio": f"$ {p.precio:.2f}",
                    "Talla": p.talla or "-",
                    "Color": p.color or "-",
                    "Categoría": p.categoria or "-",
                    "Cantidad": p.cantidad
                })
            st.dataframe(data)

    elif sub_menu == "Actualizar stock":
        for p in productos:
            nueva_cantidad = st.number_input(f"**{p.nombre}** (Stock actual: {p.cantidad})", min_value=0, value=p.cantidad, step=1)
            if st.button(f"Actualizat stock {p.nombre}"):
                dao.actualizarS(p.id, nueva_cantidad)
                st.success(f"✅ ¡Stock actualizado a {nueva_cantidad}")
