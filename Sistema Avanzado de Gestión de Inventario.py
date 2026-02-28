import os
import json
import uuid
from typing import List, Dict
from datetime import datetime

WIDTH = 94

# ==================== COLORES ====================
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_section(title: str):
    print(f"{Colors.CYAN}{title.center(WIDTH, '═')}{Colors.RESET}")


def print_big_logo():
    clear_screen()
    print(Colors.BOLD + Colors.MAGENTA)
    print("╔" + "═" * (WIDTH - 2) + "╗")
    print("║" + " SISTEMA AVANZADO DE GESTIÓN DE INVENTARIO ".center(WIDTH - 2) + "║")
    print("║" + " TIENDA PROFESIONAL - 2026 ".center(WIDTH - 2) + "║")
    print("╚" + "═" * (WIDTH - 2) + "╝")
    print(Colors.RESET)
    fecha = datetime.now().strftime('%d de %B del %Y  •  %H:%M:%S')
    print(f"{Colors.BLUE}{fecha.center(WIDTH)}{Colors.RESET}\n")


# ==================== VALIDACIONES ====================
def pedir_opcion(msg, opciones_validas):
    while True:
        op = input(msg).strip()
        if op in opciones_validas:
            return op
        print(f"{Colors.RED}Opción inválida. Intente nuevamente.{Colors.RESET}")


def pedir_texto(msg, obligatorio=True):
    while True:
        texto = input(msg).strip()
        if obligatorio and not texto:
            print(f"{Colors.RED}Campo obligatorio.{Colors.RESET}")
        else:
            return texto.title()


def pedir_entero(msg, min_val=0):
    while True:
        try:
            v = int(input(msg).strip())
            if v < min_val:
                print(f"{Colors.RED}Debe ser mayor o igual a {min_val}.{Colors.RESET}")
            else:
                return v
        except ValueError:
            print(f"{Colors.RED}Ingrese un número entero válido.{Colors.RESET}")


def pedir_float(msg, min_val=0.01):
    while True:
        try:
            v = float(input(msg).strip())
            if v < min_val:
                print(f"{Colors.RED}Debe ser mayor o igual a {min_val}.{Colors.RESET}")
            else:
                return v
        except ValueError:
            print(f"{Colors.RED}Ingrese un número válido (ej: 10.50).{Colors.RESET}")


def confirmar(msg):
    while True:
        r = input(f"{msg} (S/N): ").strip().lower()
        if r in ("s", "si"):
            return True
        if r in ("n", "no"):
            return False
        print("Ingrese S o N.")


# ==================== CLASE PRODUCTO ====================
class Producto:
    def __init__(self, id_prod, nombre, cantidad, precio, categoria="General"):
        self._id = id_prod
        self._nombre = nombre.title()
        self._cantidad = cantidad
        self._precio = precio
        self._categoria = categoria.title()
        self.fecha_agregado = datetime.now().isoformat()

    @property
    def id(self): return self._id
    @property
    def nombre(self): return self._nombre
    @property
    def cantidad(self): return self._cantidad
    @property
    def precio(self): return self._precio
    @property
    def categoria(self): return self._categoria

    @cantidad.setter
    def cantidad(self, valor):
        if valor < 0:
            raise ValueError("Cantidad negativa.")
        self._cantidad = valor

    @precio.setter
    def precio(self, valor):
        if valor < 0:
            raise ValueError("Precio negativo.")
        self._precio = valor

    def __str__(self):
        valor = self.cantidad * self.precio
        return (
            f"{Colors.CYAN}ID: {self.id}{Colors.RESET} │ "
            f"{Colors.BOLD}{self.nombre}{Colors.RESET} ({self.categoria})\n"
            f"   Cantidad: {Colors.GREEN}{self.cantidad}{Colors.RESET} │ "
            f"Precio: {Colors.YELLOW}${self.precio:.2f}{Colors.RESET} │ "
            f"Valor: {Colors.GREEN}${valor:.2f}{Colors.RESET}"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio,
            "categoria": self.categoria,
            "fecha_agregado": self.fecha_agregado
        }

    @classmethod
    def from_dict(cls, data):
        p = cls(data["id"], data["nombre"], data["cantidad"],
                data["precio"], data.get("categoria", "General"))
        p.fecha_agregado = data.get("fecha_agregado", datetime.now().isoformat())
        return p


# ==================== INVENTARIO ====================
class Inventario:
    def __init__(self, archivo="inventario.json"):
        self.archivo = archivo
        self.productos: Dict[str, Producto] = {}
        self.cargar()

    def cargar(self):
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        p = Producto.from_dict(item)
                        self.productos[p.id] = p
            except:
                print(f"{Colors.RED}Archivo corrupto. Se iniciará vacío.{Colors.RESET}")

    def guardar(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.productos.values()],
                      f, indent=4, ensure_ascii=False)

    def generar_id(self):
        pid = str(uuid.uuid4()).upper()[:8]
        while pid in self.productos:
            pid = str(uuid.uuid4()).upper()[:8]
        return pid


# ==================== PROGRAMA PRINCIPAL ====================
def main():
    inventario = Inventario()

    while True:
        print_big_logo()
        print_section(" MENÚ PRINCIPAL ")
        print("1. Añadir producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto")
        print("5. Ver inventario")
        print("6. Salir")

        opcion = pedir_opcion("Seleccione opción (1-6): ",
                              ["1", "2", "3", "4", "5", "6"])

        if opcion == "1":
            print_section(" AÑADIR PRODUCTO ")
            nombre = pedir_texto("Nombre: ")
            categoria = pedir_texto("Categoría: ", False) or "General"
            cantidad = pedir_entero("Cantidad: ", 0)
            precio = pedir_float("Precio: ", 0.01)

            pid = inventario.generar_id()
            inventario.productos[pid] = Producto(pid, nombre, cantidad, precio, categoria)
            inventario.guardar()
            print(f"{Colors.GREEN}Producto creado con ID {pid}{Colors.RESET}")

        elif opcion == "2":
            pid = pedir_texto("ID a eliminar: ")
            if pid in inventario.productos:
                if confirmar("¿Seguro que desea eliminar?"):
                    del inventario.productos[pid]
                    inventario.guardar()
                    print("Eliminado correctamente.")
            else:
                print("ID no encontrado.")

        elif opcion == "3":
            pid = pedir_texto("ID a actualizar: ")
            if pid in inventario.productos:
                cantidad = pedir_entero("Nueva cantidad: ", 0)
                precio = pedir_float("Nuevo precio: ", 0.01)
                inventario.productos[pid].cantidad = cantidad
                inventario.productos[pid].precio = precio
                inventario.guardar()
                print("Actualizado correctamente.")
            else:
                print("Producto no encontrado.")

        elif opcion == "4":
            texto = pedir_texto("Buscar: ")
            resultados = [p for p in inventario.productos.values()
                          if texto.lower() in p.nombre.lower()]
            for p in resultados:
                print(p)

        elif opcion == "5":
            for p in inventario.productos.values():
                print(p)

        elif opcion == "6":
            print("Saliendo del sistema...")
            break

        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma cerrado por el usuario.")