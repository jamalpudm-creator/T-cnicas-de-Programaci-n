"""
Funcionabilidad: Sistema para calcular áreas de figuras geométricas
Detalles: Este programa permite al usuario seleccionar una figura geométrica basica
y obtener el cálculo de su área de manera precisas.
"""

import math  # Librería para operaciones matemáticas

# Variable booleana que indica si el programa continúa ejecutándose
ejecucion_activa = True

while ejecucion_activa:
#Menú del usuario
    print("\nElija una figura para conocer su área:")
    print("1. Círculo")
    print("2. Cuadrado")
    print("3. Triángulo")
    print("4. Rectángulo")
    print("5. Rombo")
    print("6. Terminar programa")

    opcion = int(input("Seleccione una opción válida (1-6): "))

    if opcion == 1:
        # gráfica del círculo
        print("""
            *****
         **           **
       **               **
       **               **
         **           **
            *****
        """)

        radio = float(input("Digite el valor del radio: "))
        area = math.pi * radio ** 2
        print(f"El área correspondiente del círculo es: {area:.2f}")

    elif opcion == 2:
        #  gráfica del cuadrado
        print("""
        +---------+
        |         |
        |         |
        |         |
        +---------+
        """)

        lado = float(input("Ingrese la medida del lado: "))
        area = lado * lado
        print(f"El área total del cuadrado es: {area:.2f}")

    elif opcion == 3:
        # gráfica del triángulo
        print("""
             /\\
            /  \\
           /    \\
          /______\\
        """)

        base = float(input("Ingrese el valor de la base: "))
        altura = float(input("Ingrese el valor de la altura: "))
        area = (base * altura) / 2
        print(f"El área resultante del triángulo es: {area:.2f}")

    elif opcion == 4:
        #  gráfica del rectángulo
        print("""
        +--------------+
        |              |
        |              |
        +--------------+
        """)

        base = float(input("Ingrese la medida de la base: "))
        altura = float(input("Ingrese la medida de la altura: "))
        area = base * altura
        print(f"El área calculada del rectángulo es: {area:.2f}")

    elif opcion == 5:
        #  gráfica del rombo
        print("""
              /\\
             <  >
              \\/
        """)

        diagonal_mayor = float(input("Ingrese la diagonal mayor: "))
        diagonal_menor = float(input("Ingrese la diagonal menor: "))
        area = (diagonal_mayor * diagonal_menor) / 2
        print(f"El área obtenida del rombo es: {area:.2f}")

    elif opcion == 6:
        ejecucion_activa = False
        print("El programa ha finalizado correctamente.")

    else:
        print("La opción ingresada no es válida. Intente nuevamente.")
