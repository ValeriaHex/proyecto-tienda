import os

def mostrar_menu():
        os.system('cls' if os.name == 'nt' else 'clear')
        print(" ╔══════════════════════════════════════════╗")
        print(" ║         🛒 GESTIÓN DE TIENDA 🛒          ║")
        print(" ╠══════════════════════════════════════════╣")
        print(" ║  1. 🧾 Gestionar productos               ║")
        print(" ║  2. 👤 Gestionar clientes                ║")
        print(" ║  3. 💰 Gestionar ventas                  ║")
        print(" ║  4. 📦 Gestionar inventario              ║")
        print(" ║  5. ❌ Salir                             ║")
        print(" ╚══════════════════════════════════════════╝")

        op = input(" 💎 Seleccione una opcion: ")
        return op
