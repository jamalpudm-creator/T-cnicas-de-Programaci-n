# ==========================================================
# SISTEMA DE GESTION DE INVENTARIO
# VERSION CON PERSISTENCIA EN ARCHIVO Y MANEJO DE ERRORES
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
# CLASE INVENTARIO CON ARCHIVOS
# ==========================================================
class Inventario:

    def __init__(self, archivo="inventario.txt"):
        self.__productos = []
        self.__archivo = archivo
        self.cargar_desde_archivo()  # Se carga automáticamente al iniciar

    # ================= CARGA DE DATOS =================
    def cargar_desde_archivo(self):
        """
        Lee el archivo de inventario y reconstruye la lista de productos.
        Si el archivo no existe, lo crea automáticamente.
        """

        try:
            if not os.path.exists(self.__archivo):
                # Crear archivo vacío si no existe
                open(self.__archivo, "w").close()
                print(Color.AMARILLO + "\n[ℹ] Archivo de inventario creado automáticamente." + Color.RESET)
                return

            with open(self.__archivo, "r", encoding="utf-8") as f:
                for linea in f:
                    try:
                        id_p, nombre, cantidad, precio = linea.strip().split("|")
                        producto = Producto(id_p, nombre, int(cantidad), float(precio))
                        self.__productos.append(producto)
                    except ValueError:
                        print(Color.ROJO + "\n[⚠] Línea corrupta ignorada en archivo." + Color.RESET)

        except PermissionError:
            print(Color.ROJO + "\n[✖] Error: Sin permisos para leer el archivo." + Color.RESET)
        except Exception as e:
            print(Color.ROJO + f"\n[✖] Error inesperado al cargar archivo: {e}" + Color.RESET)

    # ================= GUARDAR DATOS =================
    def guardar_en_archivo(self):
        """
        Reescribe completamente el archivo con el estado actual del inventario.
        Se ejecuta después de cada modificación.
        """

        try:
            with open(self.__archivo, "w", encoding="utf-8") as f:
                for p in self.__productos:
                    linea = f"{p.get_id()}|{p.get_nombre()}|{p.get_cantidad()}|{p.get_precio()}\n"
                    f.write(linea)

            print(Color.CYAN + "[💾] Cambios guardados en archivo correctamente." + Color.RESET)

        except PermissionError:
            print(Color.ROJO + "\n[✖] Error: No tiene permisos para escribir en el archivo." + Color.RESET)
        except IOError:
            print(Color.ROJO + "\n[✖] Error de entrada/salida al guardar archivo." + Color.RESET)

    # ================= FUNCIONES PRINCIPALES =================
    def buscar_por_id(self, id_producto):
        for p in self.__productos:
            if p.get_id() == id_producto:
                return p
        return None

    def añadir_producto(self, producto):
        if self.buscar_por_id(producto.get_id()):
            print(Color.ROJO + "\n[✖] ID ya existente." + Color.RESET)
            return

        self.__productos.append(producto)
        print(Color.VERDE + "\n[✔] Producto agregado." + Color.RESET)
        self.guardar_en_archivo()

    def eliminar_producto(self, id_producto):
        producto = self.buscar_por_id(id_producto)
        if producto:
            self.__productos.remove(producto)
            print(Color.VERDE + "\n[✔] Producto eliminado." + Color.RESET)
            self.guardar_en_archivo()
        else:
            print(Color.ROJO + "\n[✖] Producto no encontrado." + Color.RESET)

    def actualizar_producto(self, id_producto, cantidad, precio):
        producto = self.buscar_por_id(id_producto)
        if producto:
            producto.set_cantidad(cantidad)
            producto.set_precio(precio)
            print(Color.VERDE + "\n[✔] Producto actualizado." + Color.RESET)
            self.guardar_en_archivo()
        else:
            print(Color.ROJO + "\n[✖] Producto no encontrado." + Color.RESET)

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
        print("║      SISTEMA DE INVENTARIO CON ARCHIVOS             ║")
        print("╚══════════════════════════════════════════════════════╝")
        print(Color.RESET)

        print(" 1 ➤ Añadir Repuesto")
        print(" 2 ➤ Eliminar Repuesto")
        print(" 3 ➤ Actualizar Repuesto")
        print(" 4 ➤ Mostrar Inventario")
        print(" 5 ➤ Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            try:
                id_p = input("ID: ")
                nombre = input("Nombre: ")
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))
                inventario.añadir_producto(Producto(id_p, nombre, cantidad, precio))
            except ValueError:
                print(Color.ROJO + "\nDatos inválidos." + Color.RESET)
            pausa()

        elif opcion == "2":
            id_p = input("ID: ")
            inventario.eliminar_producto(id_p)
            pausa()

        elif opcion == "3":
            try:
                id_p = input("ID: ")
                cantidad = int(input("Nueva cantidad: "))
                precio = float(input("Nuevo precio: "))
                inventario.actualizar_producto(id_p, cantidad, precio)
            except ValueError:
                print(Color.ROJO + "\nDatos inválidos." + Color.RESET)
            pausa()

        elif opcion == "4":
            inventario.mostrar_inventario()
            pausa()

        elif opcion == "5":
            print(Color.AMARILLO + "\nGracias por usar el sistema." + Color.RESET)
            break

        else:
            print(Color.ROJO + "\nOpción inválida." + Color.RESET)
            pausa()


# ==========================================================
# EJECUCION
# ==========================================================
if __name__ == "__main__":
    menu()
