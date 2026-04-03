import tkinter as tk
from tkinter import ttk, messagebox
import json, os
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas - UI Pro")
        self.root.geometry("750x650")
        self.root.minsize(650, 600)

        # Tema moderno
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()

        self.file = "tasks.json"
        self.tasks = []
        self.filtered_tasks = []
        self.load_tasks()

        # ================== CONTENEDOR ==================
        main = ttk.Frame(root, padding=15, style="Main.TFrame")
        main.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(main, text="Gestor de Tareas", style="Title.TLabel")
        title.pack(anchor="center", pady=(0, 10))

        # ================== INPUT ==================
        input_frame = ttk.Frame(main, style="Card.TFrame")
        input_frame.pack(fill=tk.X, pady=5)

        self.entry = ttk.Entry(input_frame, font=("Segoe UI", 11))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=10)

        self.date_entry = ttk.Entry(input_frame, width=12)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.pack(side=tk.LEFT, padx=5)

        self.category = ttk.Combobox(input_frame, values=["General", "Estudio", "Trabajo"], width=12)
        self.category.set("General")
        self.category.pack(side=tk.LEFT, padx=5)

        ttk.Button(input_frame, text="Añadir", command=self.add_task, style="Accent.TButton").pack(side=tk.LEFT, padx=5)

        # ================== BUSCADOR ==================
        search_frame = ttk.Frame(main)
        search_frame.pack(fill=tk.X, pady=5)

        ttk.Label(search_frame, text="Buscar:", style="Text.TLabel").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.filter_tasks())
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # ================== LISTA ==================
        list_frame = ttk.Frame(main, style="Card.TFrame")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tree = ttk.Treeview(list_frame, columns=("Fecha", "Categoria", "Estado", "Tarea"), show="headings")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Categoria", text="Categoría")
        self.tree.heading("Estado", text="Estado")
        self.tree.heading("Tarea", text="Tarea")

        self.tree.column("Fecha", width=100, anchor="center")
        self.tree.column("Categoria", width=100, anchor="center")
        self.tree.column("Estado", width=80, anchor="center")
        self.tree.column("Tarea", width=300)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ================== BOTONES ==================
        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="Completar (C)", command=self.complete_task).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)
        ttk.Button(btn_frame, text="Eliminar (Del)", command=self.delete_task).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)
        ttk.Button(btn_frame, text="Limpiar", command=self.clear_all).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)

        # ================== STATS ==================
        self.stats = ttk.Label(main, text="", style="Stats.TLabel")
        self.stats.pack(pady=5)

        # Atajos
        root.bind("<Return>", lambda e: self.add_task())
        root.bind("c", lambda e: self.complete_task())
        root.bind("<Delete>", lambda e: self.delete_task())
        root.bind("<Escape>", lambda e: root.quit())

        self.update_list()

    # ================== ESTILOS ==================
    def configure_styles(self):
        self.style.configure("Main.TFrame", background="#f4f6f9")
        self.style.configure("Card.TFrame", background="white", relief="flat")
        self.style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"), foreground="#333")
        self.style.configure("Text.TLabel", font=("Segoe UI", 10))
        self.style.configure("Stats.TLabel", font=("Segoe UI", 10, "bold"))
        self.style.configure("Accent.TButton", background="#4CAF50", foreground="white")

    # ================== FUNCIONES ==================
    def add_task(self):
        text = self.entry.get().strip()
        if not text:
            messagebox.showwarning("Aviso", "Escribe una tarea")
            return

        self.tasks.append({
            "text": text,
            "done": False,
            "date": self.date_entry.get(),
            "category": self.category.get()
        })

        self.entry.delete(0, tk.END)
        self.update_list()
        self.save_tasks()

    def complete_task(self):
        try:
            i = self.tree.selection()[0]
            index = int(i)
            self.tasks[index]["done"] = not self.tasks[index]["done"]
            self.update_list()
            self.save_tasks()
        except:
            messagebox.showwarning("Aviso", "Selecciona una tarea")

    def delete_task(self):
        try:
            i = self.tree.selection()[0]
            index = int(i)
            del self.tasks[index]
            self.update_list()
            self.save_tasks()
        except:
            messagebox.showwarning("Aviso", "Selecciona una tarea")

    def clear_all(self):
        if messagebox.askyesno("Confirmar", "¿Eliminar todas?"):
            self.tasks.clear()
            self.update_list()
            self.save_tasks()

    def filter_tasks(self):
        keyword = self.search_var.get().lower()
        self.filtered_tasks = [t for t in self.tasks if keyword in t["text"].lower()]
        self.update_list(filtered=True)

    def update_list(self, filtered=False):
        for i in self.tree.get_children():
            self.tree.delete(i)

        data = self.filtered_tasks if filtered else self.tasks

        for idx, t in enumerate(data):
            estado = "✔" if t["done"] else "✗"
            self.tree.insert("", "end", iid=str(idx), values=(t["date"], t["category"], estado, t["text"]))

        self.update_stats()

    def update_stats(self):
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t["done"])
        self.stats.config(text=f"Total: {total} | Completadas: {done}")

    # ================== ARCHIVOS ==================
    def save_tasks(self):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=4)

    def load_tasks(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
            except:
                self.tasks = []

# ================== RUN ==================
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
