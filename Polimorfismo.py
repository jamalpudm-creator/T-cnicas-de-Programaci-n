# Clases diferentes pero con el mismo método accion()

class BalonFutbol:
    def accion(self):
        return "El balón rueda por la cancha."


class CarroJuguete:
    def accion(self):
        return "El carro de juguete avanza al ser empujado."


class Peluche:
    def accion(self):
        return "El peluche se queda quieto y suave."


# Función polimórfica
def mostrar_accion(objeto):
    print(objeto.accion())


# Uso
futbol = BalonFutbol()
carro = CarroJuguete()
peluche = Peluche()

mostrar_accion(futbol)
mostrar_accion(carro)
mostrar_accion(peluche)