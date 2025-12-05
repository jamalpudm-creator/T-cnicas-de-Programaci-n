# Clase base
class Juguete:
    def __init__(self, nombre):
        self.nombre = nombre

    def descripcion(self):
        return f"Esto es un juguete llamado {self.nombre}."


# Clase hija 1
class Carrito(Juguete):
    def mover(self):
        return "El carrito avanza rápidamente."


# Clase hija 2
class Muñeca(Juguete):
    def hablar(self):
        return "La muñeca dice: ¡Hola!"


# Uso
c = Carrito("Hot Wheels")
m = Muñeca("Barbie")

print(c.descripcion())
print(c.mover())

print(m.descripcion())
print(m.hablar())