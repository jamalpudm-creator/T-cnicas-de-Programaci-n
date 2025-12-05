from abc import ABC, abstractmethod

# Clase abstracta que representa a un jugador de fútbol
class Jugador(ABC):

    @abstractmethod
    def jugar(self):
        pass


# Jugador específico
class Delantero(Jugador):
    def jugar(self):
        return "El delantero dispara al arco."


class Portero(Jugador):
    def jugar(self):
        return "El portero ataja el balón."


# Uso de clases
d = Delantero()
p = Portero()

print(d.jugar())
print(p.jugar())