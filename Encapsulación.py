class Carro:
    def __init__(self, marca, gasolina):
        self.marca = marca
        self.__gasolina = gasolina  # Atributo privado

    # Método para agregar gasolina de manera controlada
    def recargar(self, cantidad):
        self.__gasolina += cantidad

    # Método para acceder al valor sin modificarlo
    def obtener_gasolina(self):
        return self.__gasolina


# Uso
carro = Carro("Toyota", 20)
carro.recargar(10)  # Aumentamos gasolina usando un método seguro

print("Gasolina actual:", carro.obtener_gasolina())