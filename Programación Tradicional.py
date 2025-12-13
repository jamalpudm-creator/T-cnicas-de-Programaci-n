# Temperaturas

def ingresar_temperaturas_diarias():

    temperaturas = []  # Lista vacía para almacenar las temperaturas
    print("Ingrese las temperaturas diarias de la semana (en grados Celsius):")

    for dia in range(1, 8):  # Bucle para los 7 días
        while True:  # Bucle para validar que sea un número válido
            try:
                temp = float(input(f"Día {dia}: "))
                if -50 <= temp <= 60:  #  temperaturas realistas
                    temperaturas.append(temp)
                    break
                else:
                    print("Error: Ingrese una temperatura entre -50 y 60°C.")
            except ValueError:
                print("Error: Ingrese un número válido.")

    return temperaturas  # Retorna la lista completa


def calcular_promedio_semanal(temperaturas):

    if len(temperaturas) != 7:
        print("Error: Debe haber exactamente 7 temperaturas.")
        return None  # Manejo de error básico

    suma = 0.0  # Variable para acumular la suma
    for temp in temperaturas:  # Bucle para sumar cada temperatura
        suma += temp

    promedio = suma / 7  # Cálculo del promedio
    return promedio  # Retorna el promedio


# Bloque principal (main) - Lógica general del programa
if __name__ == "__main__":
    print("=== Calculadora de Promedio Semanal de Temperaturas ===\n")

    # Paso 1: Ingreso de datos (llamada a la función de entrada)
    lista_temperaturas = ingresar_temperaturas_diarias()

    # Paso 2: Cálculo del promedio (llamada a la función de cálculo)
    promedio = calcular_promedio_semanal(lista_temperaturas)

    # Paso 3: Mostrar resultado
    if promedio is not None:
        print(f"\nLas temperaturas ingresadas son: {lista_temperaturas}")
        print(f"El promedio semanal es: {promedio:.2f}°C")  # Formateo a 2 decimales
    else:
        print("No se pudo calcular el promedio debido a un error en los datos.")

    print("\nPrograma finalizado.")