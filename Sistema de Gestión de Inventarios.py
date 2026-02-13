# ==========================================================
# SISTEMA DE GESTION DE INVENTARIO
# TIENDA DE REPUESTOS AUTOMOTRICES
# VERSION CON INTERFAZ PROFESIONAL MEJORADA
# ==========================================================

import os

# ================= COLORES =================
class Color:
    RESET = "\033[0m"
    ROJO = "\033[91m"
    VERDE = "\033[92m"
    AMARILLO = "\033[93m"
    AZUL = "\033[94m"
    CYAN = "\033[96m"
    NEGRITA = "\033[1m"


# ==========================================================
# CLASE PRODUCTO
# ==========================================================
class Producto:

    def __init__(self, id_producto, nombre, cantidad, precio):
        self.__id = id_producto
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio = precio

    def get_id(self):
        return self.__id

    def get_nombre(self):
        return self.__nombre

    def get_cantidad(self):
        return self.__cantidad

    def get_precio(self):
        return self.__precio

    def set_cantidad(self, cantidad):
        if cantidad >= 0:
            self.__cantidad = cantidad

    def set_precio(self, precio):
        if precio >= 0:
            self.__precio = precio

    def __str__(self):
        return (f"{self.__id:^10} | "
                f"{self.__nombre:<25} | "
                f"{self.__cantidad:^10} | "
                f"${self.__precio:>8.2f}")


# ==========================================================
# CLASE INVENTARIO
# ==========================================================
class Inventario:

    def __init__(self):
        self.__productos = []

    def buscar_por_id(self, id_producto):
        for p in self.__productos:
            if p.get_id() == id_producto:
                return p
        return None

    def añadir_producto(self, producto):
        if self.buscar_por_id(producto.get_id()):
            print(Color.ROJO + "\n[✖] ERROR: ID ya existente." + Color.RESET)
            return

        self.__productos.append(producto)
        print(Color.VERDE + "\n[✔] Producto agregado correctamente." + Color.RESET)

    def eliminar_producto(self, id_producto):
        producto = self.buscar_por_id(id_producto)

        if producto:
            self.__productos.remove(producto)
            print(Color.VERDE + "\n[✔] Producto eliminado." + Color.RESET)
        else:
            print(Color.ROJO + "\n[✖] Producto no encontrado." + Color.RESET)

    def actualizar_producto(self, id_producto, cantidad, precio):
        producto = self.buscar_por_id(id_producto)

        if producto:
            producto.set_cantidad(cantidad)
            producto.set_precio(precio)
            print(Color.VERDE + "\n[✔] Producto actualizado." + Color.RESET)
        else:
            print(Color.ROJO + "\n[✖] Producto no encontrado." + Color.RESET)

    def buscar_por_nombre(self, nombre):
        return [p for p in self.__productos if nombre.lower() in p.get_nombre().lower()]

    def mostrar_inventario(self):
        if not self.__productos:
            print(Color.AMARILLO + "\n⚠ Inventario vacío." + Color.RESET)
            return

        print(Color.CYAN + "\n" + "═"*75)
        print("         INVENTARIO DE REPUESTOS AUTOMOTRICES")
        print("═"*75 + Color.RESET)

        print(f"{'ID':^10} | {'NOMBRE':^25} | {'CANTIDAD':^10} | {'PRECIO':^10}")
        print("-"*75)

        for p in self.__productos:
            print(p)

        print("═"*75)


# ==========================================================
# FUNCIONES AUXILIARES
# ==========================================================
def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def pausa():
    input("\nPresione ENTER para continuar...")


# ==========================================================
# MENU PRINCIPAL
# ==========================================================
def menu():

    inventario = Inventario()

    while True:
        limpiar()

        print(Color.AZUL + Color.NEGRITA)
        print("╔══════════════════════════════════════════════════════╗")
        print("║        SISTEMA DE GESTION - REPUESTOS AUTOS         ║")
        print("╚══════════════════════════════════════════════════════╝")
        print(Color.RESET)

        print(" 1 ➤ Añadir Repuesto")
        print(" 2 ➤ Eliminar Repuesto")
        print(" 3 ➤ Actualizar Repuesto")
        print(" 4 ➤ Buscar Repuesto")
        print(" 5 ➤ Mostrar Inventario")
        print(" 6 ➤ Salir")
        print("────────────────────────────────────────────────────────")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            try:
                id_p = input("ID: ")
                nombre = input("Nombre del repuesto: ")
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))

                inventario.añadir_producto(Producto(id_p, nombre, cantidad, precio))

            except:
                print(Color.ROJO + "\nDatos inválidos." + Color.RESET)

            pausa()

        elif opcion == "2":
            id_p = input("ID del producto: ")
            inventario.eliminar_producto(id_p)
            pausa()

        elif opcion == "3":
            try:
                id_p = input("ID del producto: ")
                cantidad = int(input("Nueva cantidad: "))
                precio = float(input("Nuevo precio: "))
                inventario.actualizar_producto(id_p, cantidad, precio)
            except:
                print(Color.ROJO + "\nDatos inválidos." + Color.RESET)

            pausa()

        elif opcion == "4":
            nombre = input("Nombre a buscar: ")
            resultados = inventario.buscar_por_nombre(nombre)

            if resultados:
                print(Color.CYAN + "\nResultados encontrados:\n" + Color.RESET)
                for r in resultados:
                    print(r)
            else:
                print(Color.ROJO + "\nNo se encontraron coincidencias." + Color.RESET)

            pausa()

        elif opcion == "5":
            inventario.mostrar_inventario()
            pausa()

        elif opcion == "6":
            print(Color.AMARILLO + "\nGracias por utilizar el sistema." + Color.RESET)
            break

        else:
            print(Color.ROJO + "\nOpción inválida." + Color.RESET)
            pausa()


# ==========================================================
# EJECUCION
# ==========================================================
if __name__ == "__main__":
    menu()
