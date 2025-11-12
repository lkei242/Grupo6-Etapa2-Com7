# VentanaNotificaciones.py
import tkinter as tk
from tkinter import ttk, messagebox

class VentanaNotificaciones(tk.Toplevel):
    def __init__(self, master, db):
        super().__init__(master)
        self.db = db
        self.title("🔔 Notificaciones pendientes")
        self.geometry("500x350")
        self.config(bg="#f2faff")
        self.crear_widgets()

    def crear_widgets(self):
        ttk.Label(self, text="Tareas pendientes de notificar", font=("Segoe UI", 12, "bold")).pack(pady=10)

        # Contenedor del Treeview
        contenedor = ttk.Frame(self)
        contenedor.pack(fill="both", expand=True, padx=10, pady=5)

        scrollbar = ttk.Scrollbar(contenedor, orient="vertical")
        self.tree = ttk.Treeview(contenedor, columns=("fecha", "notas"), show="headings")
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        self.tree.heading("fecha", text="Fecha y Hora")
        self.tree.heading("notas", text="Notas")

        ttk.Button(self, text="🔄 Actualizar", command=self.cargar_datos).pack(pady=10)
        self.cargar_datos()

    def cargar_datos(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        tareas = self.db.tareas_para_notificar()
        if not tareas:
            messagebox.showinfo("Sin notificaciones", "No hay tareas pendientes de notificar.")
            return
        for t in tareas:
            self.tree.insert("", "end", iid=t[0], values=(t[2], t[3]))
