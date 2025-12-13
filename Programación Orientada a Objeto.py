
class ClimaSemanal:

    def __init__(self):
        """
        Constructor: Inicializa el objeto con una lista vacía de temperaturas.
        Atributo privado: _temperaturas (lista de floats).
        """
        self._temperaturas = []  # Lista encapsulada (privada) para las 7 temperaturas

    def ingresar_temperatura_diaria(self, dia, temperatura):

        if not (1 <= dia <= 7):
            raise ValueError(f"Error: El día debe estar entre 1 y 7. Ingresado: {dia}")

        if not (-50 <= temperatura <= 60):
            raise ValueError(f"Error: La temperatura debe estar entre -50 y 60°C. Ingresada: {temperatura}")

        # Encapsulamiento: reemplaza si ya existe, o agrega si no
        if len(self._temperaturas) < dia:
            # Si la lista es más corta, rellena con None temporalmente
            while len(self._temperaturas) < dia:
                self._temperaturas.append(None)
            self._temperaturas[dia - 1] = temperatura  # Índice 0-based
        else:
            self._temperaturas[dia - 1] = temperatura  # Reemplaza si ya existe

        print(f"Temperatura para el día {dia} guardada: {temperatura}°C")

    def calcular_promedio_semanal(self):
        """
        Método para calcular el promedio de las 7 temperaturas.
        Retorna el promedio (float) o None si no hay 7 datos válidos.
        """
        if len(self._temperaturas) != 7 or None in self._temperaturas:
            print("Error: Deben ingresarse exactamente 7 temperaturas válidas.")
            return None

        suma = sum(self._temperaturas)  # Suma usando built-in sum() para simplicidad
        promedio = suma / 7  # Cálculo del promedio
        return promedio

    def obtener_temperaturas(self):
        """
        Getter (método de acceso) para obtener la lista de temperaturas.
        Retorna una copia de la lista para no exponer el atributo privado.
        """
        return self._temperaturas[:]  # Copia superficial para encapsulamiento


# Bloque principal (main) - Uso del objeto POO
if __name__ == "__main__":
    print("=== Calculadora de Promedio Semanal de Temperaturas (POO) ===\n")

    # Creación de instancia (objeto) de la clase
    semana = ClimaSemanal()

    # Paso 1: Ingreso de datos diarios (usando el método de la clase)
    print("Ingrese las temperaturas diarias de la semana (en grados Celsius):")
    for dia in range(1, 8):  # Bucle para los 7 días
        while True:  # Validación de entrada
            try:
                temp = float(input(f"Día {dia}: "))
                semana.ingresar_temperatura_diaria(dia, temp)  # Llamada al método
                break
            except ValueError as e:
                print(f"{e} Intente de nuevo.")

    # Paso 2: Cálculo del promedio (usando el método de la clase)
    promedio = semana.calcular_promedio_semanal()

    # Paso 3: Mostrar resultado
    if promedio is not None:
        temperaturas = semana.obtener_temperaturas()  # Uso del getter
        print(f"\nLas temperaturas ingresadas son: {temperaturas}")
        print(f"El promedio semanal es: {promedio:.2f}°C")  # Formateo a 2 decimales
    else:
        print("No se pudo calcular el promedio debido a un error en los datos.")

    print("\nPrograma finalizado.")