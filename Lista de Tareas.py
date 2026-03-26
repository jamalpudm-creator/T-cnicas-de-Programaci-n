import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import json
import os

ARCHIVO = "tareas.json"

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDo App PRO 🔥")
        self.root.geometry("550x650")
        self.root.config(bg="#1e272e")

        self.tareas = []
        self.filtro = "todas"

        self.cargar_datos()
        self.crear_interfaz()
        self.actualizar()

    # ===== INTERFAZ =====
    def crear_interfaz(self):
        tk.Label(self.root, text="📝 Mis Tareas",
                 font=("Segoe UI", 20, "bold"),
                 bg="#1e272e", fg="white").pack(pady=10)

        # INPUT
        frame_input = tk.Frame(self.root, bg="#1e272e")
        frame_input.pack(padx=20, fill="x")

        self.entry = tk.Entry(frame_input, font=("Segoe UI", 12),
                              bg="#2f3640", fg="white", insertbackground="white")
        self.entry.pack(side="left", fill="x", expand=True, padx=(0,10), ipady=6)
        self.entry.bind("<Return>", self.agregar)

        self.fecha = DateEntry(frame_input, width=10)
        self.fecha.pack(side="left", padx=5)

        tk.Button(frame_input, text="➕", bg="#00a8ff", fg="white",
                  width=4, command=self.agregar).pack(side="right")

        # FILTROS
        frame_filtro = tk.Frame(self.root, bg="#1e272e")
        frame_filtro.pack(pady=10)

        tk.Button(frame_filtro, text="Todas", command=lambda: self.cambiar_filtro("todas")).grid(row=0, column=0, padx=5)
        tk.Button(frame_filtro, text="Pendientes", command=lambda: self.cambiar_filtro("pendientes")).grid(row=0, column=1, padx=5)
        tk.Button(frame_filtro, text="Completadas", command=lambda: self.cambiar_filtro("completadas")).grid(row=0, column=2, padx=5)

        # LISTA
        frame_lista = tk.Frame(self.root, bg="#1e272e")
        frame_lista.pack(padx=20, fill="both", expand=True)

        self.lista = tk.Listbox(frame_lista, font=("Segoe UI", 12),
                               bg="#2f3640", fg="white",
                               selectbackground="#00a8ff")
        self.lista.pack(fill="both", expand=True)
        self.lista.bind("<Double-Button-1>", self.marcar)

        # BOTONES
        frame_btn = tk.Frame(self.root, bg="#1e272e")
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="✔ Completar", bg="#4cd137", fg="white",
                  width=18, command=self.marcar).grid(row=0, column=0, padx=5)

        tk.Button(frame_btn, text="🗑 Eliminar", bg="#e84118", fg="white",
                  width=18, command=self.eliminar).grid(row=0, column=1, padx=5)

        # CONTADOR
        self.label_contador = tk.Label(self.root, text="",
                                      bg="#1e272e", fg="white",
                                      font=("Segoe UI", 10))
        self.label_contador.pack(pady=5)

    # ===== FUNCIONES =====
    def agregar(self, event=None):
        texto = self.entry.get().strip()
        if not texto:
            messagebox.showwarning("Aviso", "Escribe una tarea")
            return

        tarea = {
            "texto": texto,
            "fecha": self.fecha.get(),
            "done": False
        }

        self.tareas.append(tarea)
        self.entry.delete(0, tk.END)

        self.guardar_datos()
        self.actualizar()

    def marcar(self, event=None):
        sel = self.lista.curselection()
        if not sel:
            return

        i = sel[0]
        tareas_filtradas = self.obtener_filtradas()
        tarea_real = tareas_filtradas[i]

        tarea_real["done"] = not tarea_real["done"]

        self.guardar_datos()
        self.actualizar()

    def eliminar(self):
        sel = self.lista.curselection()
        if not sel:
            return

        i = sel[0]
        tareas_filtradas = self.obtener_filtradas()
        tarea_real = tareas_filtradas[i]

        self.tareas.remove(tarea_real)

        self.guardar_datos()
        self.actualizar()

    def actualizar(self):
        self.lista.delete(0, tk.END)

        tareas = self.obtener_filtradas()

        for t in tareas:
            icon = "✅" if t["done"] else "⬜"
            texto = f"{icon} {t['texto']} ({t['fecha']})"
            self.lista.insert(tk.END, texto)

            if t["done"]:
                idx = self.lista.size() - 1
                self.lista.itemconfig(idx, fg="#7f8c8d")

        # contador
        total = len(self.tareas)
        completadas = sum(1 for t in self.tareas if t["done"])
        self.label_contador.config(
            text=f"Total: {total} | Completadas: {completadas}"
        )

    def cambiar_filtro(self, tipo):
        self.filtro = tipo
        self.actualizar()

    def obtener_filtradas(self):
        if self.filtro == "pendientes":
            return [t for t in self.tareas if not t["done"]]
        elif self.filtro == "completadas":
            return [t for t in self.tareas if t["done"]]
        return self.tareas

    # ===== ARCHIVOS =====
    def guardar_datos(self):
        with open(ARCHIVO, "w") as f:
            json.dump(self.tareas, f)

    def cargar_datos(self):
        if os.path.exists(ARCHIVO):
            with open(ARCHIVO, "r") as f:
                self.tareas = json.load(f)


# ===== MAIN =====
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()