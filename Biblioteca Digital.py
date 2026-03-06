import os
import json
from dataclasses import dataclass, field
from typing import Dict, List, Set
from datetime import datetime


# ====================== CONSTANTES Y COLORES ======================
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"


def clear_screen() -> None:
    """Limpia la pantalla."""
    os.system('cls' if os.name == 'nt' else 'clear')


# ====================== CLASES MODERNAS (dataclasses + type hints) ======================
@dataclass(frozen=True)
class Libro:
    titulo: str
    autor: str
    categoria: str
    isbn: str

    @property
    def info(self) -> tuple[str, str]:
        return (self.titulo, self.autor)

    def obtener_titulo(self) -> str:
        return self.titulo

    def obtener_autor(self) -> str:
        return self.autor

    def __str__(self) -> str:
        return f"{Colors.CYAN}{self.titulo}{Colors.RESET} - {self.autor} (ISBN: {self.isbn}) [{self.categoria}]"


@dataclass
class Prestamo:
    libro: Libro
    fecha_prestamo: datetime


@dataclass
class Usuario:
    nombre: str
    id_usuario: str
    libros_prestados: List[Prestamo] = field(default_factory=list)

    def __str__(self) -> str:
        return f"{Colors.YELLOW}Usuario: {self.nombre} (ID: {self.id_usuario}){Colors.RESET}"


# ====================== CLASE PRINCIPAL CON PERSISTENCIA JSON ======================
class Biblioteca:
    def __init__(self) -> None:
        self.libros: Dict[str, Libro] = {}
        self.usuarios: Dict[str, Usuario] = {}
        self.ids_usuarios: Set[str] = set()

    def guardar_datos(self) -> None:
        """Guarda TODO (libros, usuarios y préstamos con fecha) en biblioteca.json"""
        data = {
            "libros": {
                isbn: {
                    "titulo": libro.titulo,
                    "autor": libro.autor,
                    "categoria": libro.categoria,
                    "isbn": libro.isbn
                }
                for isbn, libro in self.libros.items()
            },
            "usuarios": {
                uid: {
                    "nombre": usuario.nombre,
                    "id_usuario": usuario.id_usuario,
                    "libros_prestados": [
                        {
                            "titulo": p.libro.titulo,
                            "autor": p.libro.autor,
                            "categoria": p.libro.categoria,
                            "isbn": p.libro.isbn,
                            "fecha_prestamo": p.fecha_prestamo.isoformat()
                        }
                        for p in usuario.libros_prestados
                    ]
                }
                for uid, usuario in self.usuarios.items()
            }
        }
        try:
            with open("biblioteca.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"{Colors.RED}⚠️ Error al guardar datos: {e}{Colors.RESET}")

    def cargar_datos(self) -> bool:
        """Carga los datos desde biblioteca.json. Devuelve True si cargó correctamente."""
        if not os.path.exists("biblioteca.json"):
            return False
        try:
            with open("biblioteca.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            # Cargar libros disponibles
            self.libros.clear()
            for isbn, info in data.get("libros", {}).items():
                self.libros[isbn] = Libro(
                    info["titulo"], info["autor"], info["categoria"], info["isbn"]
                )

            # Cargar usuarios y sus préstamos
            self.usuarios.clear()
            self.ids_usuarios.clear()
            for uid, info in data.get("usuarios", {}).items():
                usuario = Usuario(info["nombre"], info["id_usuario"])
                for p in info.get("libros_prestados", []):
                    libro = Libro(p["titulo"], p["autor"], p["categoria"], p["isbn"])
                    fecha = datetime.fromisoformat(p["fecha_prestamo"])
                    usuario.libros_prestados.append(Prestamo(libro, fecha))
                self.usuarios[uid] = usuario
                self.ids_usuarios.add(uid)
            return True
        except Exception as e:
            print(f"{Colors.RED}⚠️ Error al cargar datos: {e}{Colors.RESET}")
            return False

    # ====================== MÉTODOS DEL SISTEMA (iguales que antes) ======================
    def agregar_libro(self, libro: Libro) -> None:
        if libro.isbn not in self.libros:
            self.libros[libro.isbn] = libro
            print(f"{Colors.GREEN}✅ Libro añadido: {libro}{Colors.RESET}")
            self.guardar_datos()
        else:
            print(f"{Colors.RED}❌ El libro ya existe.{Colors.RESET}")

    def quitar_libro(self, isbn: str) -> None:
        if isbn in self.libros:
            libro = self.libros.pop(isbn)
            print(f"{Colors.GREEN}✅ Libro eliminado: {libro}{Colors.RESET}")
            self.guardar_datos()
        else:
            print(f"{Colors.RED}❌ Libro no encontrado.{Colors.RESET}")

    def registrar_usuario(self, usuario: Usuario) -> None:
        if usuario.id_usuario not in self.ids_usuarios:
            self.usuarios[usuario.id_usuario] = usuario
            self.ids_usuarios.add(usuario.id_usuario)
            print(f"{Colors.GREEN}✅ Usuario registrado: {usuario}{Colors.RESET}")
            self.guardar_datos()
        else:
            print(f"{Colors.RED}❌ ID de usuario ya existe.{Colors.RESET}")

    def dar_de_baja_usuario(self, id_usuario: str) -> None:
        if id_usuario in self.ids_usuarios:
            usuario = self.usuarios[id_usuario]
            if usuario.libros_prestados:
                print(f"{Colors.RED}❌ No se puede dar de baja: {usuario} tiene libros prestados.{Colors.RESET}")
                return
            self.usuarios.pop(id_usuario)
            self.ids_usuarios.remove(id_usuario)
            print(f"{Colors.GREEN}✅ Usuario dado de baja: {usuario}{Colors.RESET}")
            self.guardar_datos()
        else:
            print(f"{Colors.RED}❌ Usuario no encontrado.{Colors.RESET}")

    def prestar_libro(self, isbn: str, id_usuario: str) -> None:
        if isbn in self.libros and id_usuario in self.usuarios:
            libro = self.libros.pop(isbn)
            prestamo = Prestamo(libro, datetime.now())
            self.usuarios[id_usuario].libros_prestados.append(prestamo)
            print(f"{Colors.GREEN}✅ Libro prestado: {libro} → {self.usuarios[id_usuario]}{Colors.RESET}")
            print(f"   📅 Fecha: {prestamo.fecha_prestamo.strftime('%d/%m/%Y %H:%M')}")
            self.guardar_datos()
        else:
            print(f"{Colors.RED}❌ Libro no disponible o usuario inexistente.{Colors.RESET}")

    def devolver_libro(self, isbn: str, id_usuario: str) -> None:
        if id_usuario in self.usuarios:
            usuario = self.usuarios[id_usuario]
            for i, prestamo in enumerate(usuario.libros_prestados):
                if prestamo.libro.isbn == isbn:
                    devuelto = usuario.libros_prestados.pop(i)
                    self.libros[isbn] = devuelto.libro
                    print(f"{Colors.GREEN}✅ Libro devuelto: {devuelto.libro} ← {usuario}{Colors.RESET}")
                    print(f"   📅 Prestado el: {devuelto.fecha_prestamo.strftime('%d/%m/%Y %H:%M')}")
                    self.guardar_datos()
                    return
            print(f"{Colors.RED}❌ El usuario no tiene ese libro prestado.{Colors.RESET}")
        else:
            print(f"{Colors.RED}❌ Usuario no encontrado.{Colors.RESET}")

    def buscar_libros(self, criterio: str, valor: str) -> List[Libro]:
        valor = valor.lower()
        resultados = [
            libro for libro in self.libros.values()
            if (criterio == "titulo" and valor in libro.obtener_titulo().lower()) or
               (criterio == "autor" and valor in libro.obtener_autor().lower()) or
               (criterio == "categoria" and valor in libro.categoria.lower())
        ]
        if resultados:
            print(f"\n{Colors.BLUE}📚 Resultados encontrados ({len(resultados)}):{Colors.RESET}")
            for r in resultados:
                print(f"   • {r}")
        else:
            print(f"{Colors.YELLOW}📚 No se encontraron libros.{Colors.RESET}")
        return resultados

    def listar_libros_prestados(self, id_usuario: str) -> None:
        if id_usuario in self.usuarios:
            usuario = self.usuarios[id_usuario]
            print(f"\n{Colors.MAGENTA}📖 Libros prestados a {usuario}:{Colors.RESET}")
            if usuario.libros_prestados:
                for p in usuario.libros_prestados:
                    print(f"   • {p.libro}")
                    print(f"     📅 Prestado: {p.fecha_prestamo.strftime('%d/%m/%Y %H:%M')}")
            else:
                print(f"   {Colors.YELLOW}(Ningún libro prestado){Colors.RESET}")
        else:
            print(f"{Colors.RED}❌ Usuario no encontrado.{Colors.RESET}")

    def mostrar_libros_disponibles(self) -> None:
        print(f"\n{Colors.BLUE}📚 Libros disponibles ({len(self.libros)}):{Colors.RESET}")
        if self.libros:
            for libro in self.libros.values():
                print(f"   • {libro}")
        else:
            print(f"   {Colors.YELLOW}(No hay libros disponibles){Colors.RESET}")

    def listar_usuarios(self) -> None:
        print(f"\n{Colors.MAGENTA}👥 Usuarios registrados ({len(self.usuarios)}):{Colors.RESET}")
        if self.usuarios:
            for u in self.usuarios.values():
                print(f"   • {u}")
        else:
            print(f"   {Colors.YELLOW}(No hay usuarios){Colors.RESET}")


# ====================== PROGRAMA PRINCIPAL ======================
if __name__ == "__main__":
    biblio = Biblioteca()

    # Cargar datos guardados (si existen)
    if biblio.cargar_datos():
        print(f"{Colors.GREEN}✅ Datos cargados correctamente desde biblioteca.json{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}📂 No se encontró archivo guardado. Creando datos iniciales...{Colors.RESET}")

        # ====================== 15 LIBROS PRECARGADOS ======================
        libros_precargados = [
            Libro("El Quijote", "Miguel de Cervantes", "Clásico", "978-3-16-148410-0"),
            Libro("1984", "George Orwell", "Distopía", "978-0-452-28423-4"),
            Libro("Cien años de soledad", "Gabriel García Márquez", "Realismo mágico", "978-0-06-088328-7"),
            Libro("Harry Potter y la piedra filosofal", "J.K. Rowling", "Fantasía", "978-0-7475-3269-9"),
            Libro("El Señor de los Anillos", "J.R.R. Tolkien", "Fantasía", "978-0-618-64015-7"),
            Libro("Crimen y castigo", "Fiódor Dostoyevski", "Clásico", "978-0-14-044913-6"),
            Libro("Orgullo y prejuicio", "Jane Austen", "Romance", "978-0-14-143951-8"),
            Libro("El Gran Gatsby", "F. Scott Fitzgerald", "Clásico", "978-0-7432-7356-5"),
            Libro("Donde los árboles cantan", "Laura Gallego", "Fantasía juvenil", "978-84-204-1234-5"),
            Libro("La sombra del viento", "Carlos Ruiz Zafón", "Misterio", "978-84-01-33390-3"),
            Libro("Ready Player One", "Ernest Cline", "Ciencia ficción", "978-0-307-88472-5"),
            Libro("Dune", "Frank Herbert", "Ciencia ficción", "978-0-441-17271-9"),
            Libro("El nombre del viento", "Patrick Rothfuss", "Fantasía", "978-84-01-33648-5"),
            Libro("Sapiens: De animales a dioses", "Yuval Noah Harari", "Historia", "978-84-9998-432-0"),
            Libro("El psicoanalista", "John Katzenbach", "Thriller", "978-84-01-33612-6"),
        ]

        for libro in libros_precargados:
            biblio.agregar_libro(libro)

        # ====================== USUARIOS QUE PEDISTE ======================
        biblio.registrar_usuario(Usuario("Javier Malpud", "U001"))
        biblio.registrar_usuario(Usuario("Luis Malpud", "U002"))
        biblio.registrar_usuario(Usuario("Leonardo Malpud", "U003"))

        biblio.guardar_datos()  # Guardamos la primera vez

    # ====================== MENÚ INTERACTIVO ======================
    while True:
        clear_screen()
        print(f"{Colors.BOLD}{Colors.MAGENTA}")
        print("╔════════════════════════════════════════════════════════════════════════════╗")
        print("║                  🚀 BIBLIOTECA DIGITAL - SISTEMA PROFESIONAL               ║")
        print("╚════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}")
        print(
            f"{Colors.CYAN}📚 Libros disponibles: {len(biblio.libros):3}  |  👥 Usuarios: {len(biblio.usuarios):3}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}" + "═" * 76 + f"{Colors.RESET}")

        print(f"""
{Colors.GREEN}1. Añadir libro
2. Quitar libro
3. Registrar usuario
4. Dar de baja usuario
5. Prestar libro
6. Devolver libro
7. Buscar libros
8. Listar préstamos de un usuario (con fechas)
9. Mostrar libros disponibles
10. Listar usuarios registrados
0. Salir{Colors.RESET}
        """)
        print(f"{Colors.BOLD}{Colors.BLUE}" + "═" * 76 + f"{Colors.RESET}")

        opcion = input(f"\n{Colors.BOLD}➜ Elige una opción (0-10): {Colors.RESET}").strip()

        if opcion == "1":
            titulo = input("Título: ")
            autor = input("Autor: ")
            cat = input("Categoría: ")
            isbn = input("ISBN: ")
            biblio.agregar_libro(Libro(titulo, autor, cat, isbn))

        elif opcion == "2":
            isbn = input(f"{Colors.YELLOW}ISBN: {Colors.RESET}")
            biblio.quitar_libro(isbn)

        elif opcion == "3":
            nombre = input("Nombre: ")
            uid = input("ID usuario: ")
            biblio.registrar_usuario(Usuario(nombre, uid))

        elif opcion == "4":
            uid = input(f"{Colors.YELLOW}ID usuario: {Colors.RESET}")
            biblio.dar_de_baja_usuario(uid)

        elif opcion == "5":
            isbn = input(f"{Colors.YELLOW}ISBN: {Colors.RESET}")
            uid = input(f"{Colors.YELLOW}ID usuario: {Colors.RESET}")
            biblio.prestar_libro(isbn, uid)

        elif opcion == "6":
            isbn = input(f"{Colors.YELLOW}ISBN: {Colors.RESET}")
            uid = input(f"{Colors.YELLOW}ID usuario: {Colors.RESET}")
            biblio.devolver_libro(isbn, uid)

        elif opcion == "7":
            crit = input("Buscar por (titulo/autor/categoria): ").lower()
            val = input("Valor: ")
            if crit in ["titulo", "autor", "categoria"]:
                biblio.buscar_libros(crit, val)

        elif opcion == "8":
            uid = input(f"{Colors.YELLOW}ID usuario: {Colors.RESET}")
            biblio.listar_libros_prestados(uid)

        elif opcion == "9":
            biblio.mostrar_libros_disponibles()

        elif opcion == "10":
            biblio.listar_usuarios()

        elif opcion == "0":
            clear_screen()
            print(
                f"{Colors.GREEN}👋 ¡Gracias por usar el sistema, {list(biblio.usuarios.values())[0].nombre.split()[0] if biblio.usuarios else 'usuario'}!{Colors.RESET}")
            break

        else:
            print(f"{Colors.RED}❌ Opción inválida.{Colors.RESET}")

        input(f"\n{Colors.BOLD}{Colors.YELLOW}Presiona ENTER para continuar...{Colors.RESET}")