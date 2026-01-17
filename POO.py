
# -------- 🧱 CLASE BASE --------
class Coctel:
    def __init__(self, nombre, ingredientes):
        self.nombre = nombre
        self.ingredientes = ingredientes
        self.__precio = 0  # 🔒 Atributo privado (Encapsulación)

    # 💰 Método para establecer el precio
    def set_precio(self, precio):
        if precio > 0:
            self.__precio = precio

    # 👀 Método getter
    def get_precio(self):
        return self.__precio

    # 🍶 Método que puede ser sobrescrito (Polimorfismo)
    def preparar(self):
        print(f"🍹 Preparando el cóctel {self.nombre} con ingredientes básicos.")

    # 📋 Mostrar información
    def mostrar_info(self):
        print(f"🍸 Cóctel: {self.nombre}")
        print(f"🧾 Ingredientes: {', '.join(self.ingredientes)}")
        print(f"💲 Precio: ${self.get_precio()}")


# -------- 🧬 CLASE DERIVADA --------
class CoctelAlcoholico(Coctel):
    def __init__(self, nombre, ingredientes, grado_alcohol):
        super().__init__(nombre, ingredientes)
        self.grado_alcohol = grado_alcohol

    # 🔁 POLIMORFISMO: método sobrescrito
    def preparar(self):
        print(f"🥂 Preparando el cóctel alcohólico {self.nombre} "
              f"con {self.grado_alcohol}% de alcohol.")

    def mostrar_info(self):
        super().mostrar_info()
        print(f"🔥 Grado de alcohol: {self.grado_alcohol}%")


# -------- ▶️ PROGRAMA PRINCIPAL --------
if __name__ == "__main__":
    # 🧪 Crear objetos
    coctel1 = Coctel("Limonada Tropical", ["Limón 🍋", "Azúcar", "Agua 💧"])
    coctel2 = CoctelAlcoholico("Margarita", ["Tequila 🥃", "Limón 🍋", "Sal"], 35)

    # 💰 Establecer precios
    coctel1.set_precio(3.50)
    coctel2.set_precio(7.00)

    # 🍶 Preparación
    print("🍹 ----- Preparación de Cócteles ----- 🍹")
    coctel1.preparar()
    coctel2.preparar()

    # 📋 Información final
    print("\n📋 ----- Información de Cócteles ----- 📋")
    coctel1.mostrar_info()
    print()
    coctel2.mostrar_info()
