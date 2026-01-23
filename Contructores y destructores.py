import gc


class Vehiculo:
    """
    Clase que representa un vehículo genérico.
    Demuestra el uso de constructor y destructor en Python.
    """

    def __init__(self, marca, modelo, anio):
        """
        Constructor de la clase.

        Se ejecuta automáticamente al crear el objeto.
        Inicializa el estado del vehículo.
        """
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self._en_movimiento = False

        print(f"[INIT] Vehículo creado: {self.marca} {self.modelo} ({self.anio})")

    def arrancar(self):
        """
        Cambia el estado del vehículo a 'en movimiento'.
        """
        if not self._en_movimiento:
            self._en_movimiento = True
            print("[INFO] El vehículo ha arrancado.")

    def detener(self):
        """
        Cambia el estado del vehículo a 'detenido'.
        """
        if self._en_movimiento:
            self._en_movimiento = False
            print("[INFO] El vehículo se ha detenido.")

    def mostrar_info(self):
        """
        Muestra la información general del vehículo.
        """
        estado = "En movimiento" if self._en_movimiento else "Detenido"
        print(f"Vehículo: {self.marca} {self.modelo} ({self.anio}) - Estado: {estado}")

    def __del__(self):
        """
        Destructor de la clase.

        Se ejecuta cuando el recolector de basura elimina el objeto.
        Aquí se simula la liberación de recursos.
        """
        print(f"[DEL] Recursos liberados del vehículo {self.marca} {self.modelo}.")


# -------------------------
# Programa principal
# -------------------------

if __name__ == "__main__":
    # Creación del objeto → se ejecuta el constructor
    vehiculo = Vehiculo("Nissan", "Frontier", 2023)

    # Uso de los métodos del objeto
    vehiculo.mostrar_info()
    vehiculo.arrancar()
    vehiculo.mostrar_info()
    vehiculo.detener()
    vehiculo.mostrar_info()

    # Eliminación explícita del objeto
    del vehiculo

    # Forzamos la recolección de basura
    # SOLO con fines académicos para asegurar la ejecución del destructor
    gc.collect()
