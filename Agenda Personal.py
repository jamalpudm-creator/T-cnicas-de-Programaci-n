import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

try:
    from tkcalendar import DateEntry
except ImportError:
    DateEntry = None

class AgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda PRO")
        self.root.geometry("720x500")
        self.dark_mode = True

        self.configurar_estilos()

        # Frame entrada
        self.frame_entrada = ttk.Frame(self.root)
        self.frame_entrada.pack(pady=15)

        # ================= INPUTS =================

        # Fecha (selector)
        ttk.Label(self.frame_entrada, text="📅 Fecha:").grid(row=0, column=0, padx=10, pady=8)

        if DateEntry:
            self.fecha_entry = DateEntry(self.frame_entrada, width=16, date_pattern='yyyy-mm-dd')
        else:
            self.fecha_entry = ttk.Entry(self.frame_entrada, width=18)
            self.fecha_entry.insert(0, "Instala tkcalendar")

        self.fecha_entry.grid(row=0, column=1, padx=10, pady=8)

        # Hora (selector con Spinbox)
        ttk.Label(self.frame_entrada, text="⏰ Hora:").grid(row=1, column=0, padx=10, pady=8)

        frame_hora = ttk.Frame(self.frame_entrada)
        frame_hora.grid(row=1, column=1)

        self.hora_spin = tk.Spinbox(frame_hora, from_=0, to=23, width=5, format="%02.0f")
        self.min_spin = tk.Spinbox(frame_hora, from_=0, to=59, width=5, format="%02.0f")

        self.hora_spin.pack(side="left")
        ttk.Label(frame_hora, text=":").pack(side="left")
        self.min_spin.pack(side="left")

        # Descripción
        ttk.Label(self.frame_entrada, text="📝 Descripción:").grid(row=2, column=0, padx=10, pady=8)
        self.desc_entry = ttk.Entry(self.frame_entrada, width=40)
        self.desc_entry.grid(row=2, column=1, padx=10, pady=8)

        # Botones
        frame_botones = ttk.Frame(self.root)
        frame_botones.pack(pady=10)

        ttk.Button(frame_botones, text="➕ Agregar", command=self.agregar_evento).grid(row=0, column=0, padx=10)
        ttk.Button(frame_botones, text="🗑 Eliminar", command=self.eliminar_evento).grid(row=0, column=1, padx=10)
        ttk.Button(frame_botones, text="🧼 Limpiar", command=self.limpiar_campos).grid(row=0, column=2, padx=10)
        ttk.Button(frame_botones, text="🌗 Tema", command=self.toggle_tema).grid(row=0, column=3, padx=10)

        # Tabla
        self.tree = ttk.Treeview(self.root, columns=("Fecha", "Hora", "Descripción"), show="headings")
        for col in ("Fecha", "Hora", "Descripción"):
            self.tree.heading(col, text=col, command=lambda c=col: self.ordenar_columna(c, False))
            self.tree.column(col, anchor="center")

        self.tree.pack(expand=True, fill="both", padx=15, pady=15)

        # Barra estado
        self.status = ttk.Label(self.root, text="Listo", anchor="w")
        self.status.pack(fill="x")

    # ================= ESTILO =================
    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("default")

        if self.dark_mode:
            bg = "#1e1e2f"
            fg = "white"
            entry_bg = "#2e2e3e"
        else:
            bg = "#f5f5f5"
            fg = "black"
            entry_bg = "white"

        self.root.configure(bg=bg)

        style.configure("TLabel", background=bg, foreground=fg, font=("Segoe UI", 10))
        style.configure("TFrame", background=bg)
        style.configure("TButton", font=("Segoe UI", 10, "bold"))

        style.configure("Treeview",
                        background=entry_bg,
                        foreground=fg,
                        fieldbackground=entry_bg,
                        rowheight=25)

    def toggle_tema(self):
        self.dark_mode = not self.dark_mode
        self.configurar_estilos()

    # ================= FUNCIONES =================
    def agregar_evento(self):
        # Fecha
        if DateEntry:
            fecha = self.fecha_entry.get()
        else:
            fecha = self.fecha_entry.get().strip()

        # Hora
        hora = f"{int(self.hora_spin.get()):02d}:{int(self.min_spin.get()):02d}"

        desc = self.desc_entry.get().strip()

        if not desc:
            messagebox.showwarning("Error", "Ingrese descripción")
            return

        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except:
            messagebox.showerror("Error", "Fecha inválida")
            return

        self.tree.insert("", tk.END, values=(fecha, hora, desc))
        self.status.config(text=f"Evento agregado: {fecha} {hora}")
        self.limpiar_campos()

    def eliminar_evento(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione un elemento")
            return
        self.tree.delete(selected)
        self.status.config(text="Evento eliminado")

    def limpiar_campos(self):
        self.desc_entry.delete(0, tk.END)
        self.status.config(text="Campos limpiados")

    def ordenar_columna(self, col, reverse):
        datos = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        datos.sort(reverse=reverse)

        for index, (val, k) in enumerate(datos):
            self.tree.move(k, "", index)

        self.tree.heading(col, command=lambda: self.ordenar_columna(col, not reverse))


if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()
