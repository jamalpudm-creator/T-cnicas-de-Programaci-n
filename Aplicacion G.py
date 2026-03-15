import tkinter as tk
from tkinter import ttk

# Función para agregar datos
def agregar_dato():
    dato = entrada.get()
    if dato != "":
        tabla.insert("", "end", values=(dato,))
        entrada.delete(0, tk.END)

# Función para limpiar la tabla
def limpiar_tabla():
    for item in tabla.get_children():
        tabla.delete(item)

# Ventana principal
ventana = tk.Tk()
ventana.title("Gestor de Datos")
ventana.geometry("450x350")
ventana.config(bg="#f0f0f0")

# Título
titulo = tk.Label(
    ventana,
    text="Registro de Información",
    font=("Arial", 16, "bold"),
    bg="#f0f0f0"
)
titulo.pack(pady=10)

# Frame de entrada
frame_entrada = tk.Frame(ventana, bg="#f0f0f0")
frame_entrada.pack(pady=5)

label = tk.Label(frame_entrada, text="Ingrese un dato:", bg="#f0f0f0")
label.grid(row=0, column=0, padx=5)

entrada = tk.Entry(frame_entrada, width=25)
entrada.grid(row=0, column=1, padx=5)

# Frame de botones
frame_botones = tk.Frame(ventana, bg="#f0f0f0")
frame_botones.pack(pady=10)

boton_agregar = tk.Button(
    frame_botones,
    text="Agregar",
    width=10,
    bg="#4CAF50",
    fg="white",
    command=agregar_dato
)
boton_agregar.grid(row=0, column=0, padx=10)

boton_limpiar = tk.Button(
    frame_botones,
    text="Limpiar",
    width=10,
    bg="#f44336",
    fg="white",
    command=limpiar_tabla
)
boton_limpiar.grid(row=0, column=1, padx=10)

# Tabla
tabla = ttk.Treeview(ventana, columns=("Dato"), show="headings", height=8)
tabla.heading("Dato", text="Datos ingresados")
tabla.pack(pady=10)

# Ejecutar programa
ventana.mainloop()