import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

class FormularioTarea(tk.Toplevel):
    
    def __init__(self, master, db, colores, tarea=None):
        super().__init__(master)
        self.db = db
        self.tarea = tarea
        self.colores = colores
        self.title("✏️ Editar Tarea" if tarea else "➕ Nueva Tarea")
        self.geometry("420x440")
        self.config(bg=colores["bg_principal"])
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text="Título:", bg=self.colores["bg_principal"], fg=self.colores["fg_texto"]).pack(pady=5)
        self.titulo = tk.Entry(self, width=40, bg=self.colores["bg_secundario"], fg=self.colores["fg_texto"], insertbackground=self.colores["fg_texto"])
        self.titulo.pack(pady=5)

        tk.Label(self, text="Descripción:", bg=self.colores["bg_principal"], fg=self.colores["fg_texto"]).pack(pady=5)
        self.descripcion = tk.Entry(self, width=40, bg=self.colores["bg_secundario"], fg=self.colores["fg_texto"], insertbackground=self.colores["fg_texto"])
        self.descripcion.pack(pady=5)

        tk.Label(self, text="Fecha:", bg=self.colores["bg_principal"], fg=self.colores["fg_texto"]).pack(pady=5)
        self.fecha = DateEntry(self, width=37, background=self.colores["fg_acento"], date_pattern="yyyy-mm-dd")
        self.fecha.pack(pady=5)

        hora_frame = ttk.Frame(self)
        hora_frame.pack(pady=5)
        tk.Label(hora_frame, text="Hora:", bg=self.colores["bg_principal"], fg=self.colores["fg_texto"]).grid(row=0, column=0, padx=5)
        self.hora = tk.Spinbox(hora_frame, from_=0, to=23, width=5, format="%02.0f", bg=self.colores["bg_secundario"], fg=self.colores["fg_texto"], insertbackground=self.colores["fg_texto"])
        self.minuto = tk.Spinbox(hora_frame, from_=0, to=59, width=5, format="%02.0f", bg=self.colores["bg_secundario"], fg=self.colores["fg_texto"], insertbackground=self.colores["fg_texto"])
        self.hora.grid(row=0, column=1)
        tk.Label(hora_frame, text="Minutos:", bg=self.colores["bg_principal"], fg=self.colores["fg_texto"]).grid(row=0, column=2, padx=5)
        self.minuto.grid(row=0, column=3)

        tk.Label(self, text="Notas:", bg=self.colores["bg_principal"], fg=self.colores["fg_texto"]).pack(pady=5)
        self.notas = tk.Entry(self, width=40, bg=self.colores["bg_secundario"], fg=self.colores["fg_texto"], insertbackground=self.colores["fg_texto"])
        self.notas.pack(pady=5)

        tk.Label(self, text="Categoría:", bg=self.colores["bg_principal"], fg=self.colores["fg_texto"]).pack(pady=5)
        categorias = [c[1] for c in self.db.listar_categorias()]
        self.categoria = ttk.Combobox(self, values=categorias, state="readonly", width=37)
        self.categoria.set(categorias[0])
        self.categoria.pack(pady=5)

        ttk.Button(self, text="Guardar", command=self.guardar).pack(pady=15)

        if self.tarea:
            self.cargar_datos()

    def cargar_datos(self):
        t = self.tarea
        self.titulo.insert(0, t[1])
        self.descripcion.insert(0, t[2])
        self.notas.insert(0, t[4])
        # Controlo esto por si fecha/hora no están en el formato esperado
        try:
            fecha_str, hora_str = (t[3] or "").split(" ")
            self.fecha.set_date(datetime.strptime(fecha_str, "%Y-%m-%d"))
            h, m = hora_str.split(":")
        except Exception:
            h, m = "00", "00"
        # Esto lo que hace es asegurar un formato de dos dígitos...
        try:
            h_int = int(h)
            m_int = int(m)
        except Exception:
            h_int, m_int = 0, 0
        self.hora.delete(0, tk.END)
        self.hora.insert(0, f"{h_int:02d}")
        self.minuto.delete(0, tk.END)
        self.minuto.insert(0, f"{m_int:02d}")
        if t[6]:
            self.categoria.set(t[6])

    def guardar(self):
        titulo = self.titulo.get().strip()
        if not titulo:
            messagebox.showerror("Error", "El título es obligatorio.")
            return

        fecha = self.fecha.get_date().strftime("%Y-%m-%d")
        # Valida hora y minuto
        try:
            h = int(self.hora.get())
            m = int(self.minuto.get())
            if not (0 <= h <= 23 and 0 <= m <= 59):
                raise ValueError
        except Exception:
            messagebox.showerror("Error", "Hora inválida. Ingresa hora (0-23) y minutos (0-59).")
            return

        hora_min = f"{h:02d}:{m:02d}"
        fecha_hora = f"{fecha} {hora_min}"
        cat_nombre = self.categoria.get()

        categoria_id = None
        for c in self.db.listar_categorias():
            if c[1] == cat_nombre:
                categoria_id = c[0]
                break

        if self.tarea:
            self.db.actualizar_tarea(self.tarea[0], titulo, self.descripcion.get(), fecha_hora, self.notas.get(), categoria_id)
        else:
            self.db.agregar_tarea(titulo, self.descripcion.get(), fecha_hora, self.notas.get(), categoria_id)

        messagebox.showinfo("Éxito", "Tarea guardada correctamente.")
        self.destroy()