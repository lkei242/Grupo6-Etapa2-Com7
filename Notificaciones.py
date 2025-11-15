import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime
from plyer import notification # importacion de plyer para notificaciones del sistema operativo

class VentanaNotificaciones(tk.Toplevel):
    def __init__(self, master, db, colores):
        super().__init__(master)
        self.db = db
        self.colores = colores
        self.title("🔔 Notificaciones")
        self.geometry("500x400")
        self.config(bg=colores["bg_principal"])
        
        # Inicializar gestor de notificaciones
        self.hilo_activo = True
        self.hilo = threading.Thread(target=self.verificar_notificaciones, daemon=True)
        self.hilo.start()
        
        # Detener hilo al cerrar la ventana
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.crear_widgets()

    def crear_widgets(self):
        ttk.Label(self, text="Tareas Pendientes de Notificar", font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        tree_container = ttk.Frame(self)
        tree_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_container, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(tree_container, columns=("titulo", "fecha", "desc"), show="headings", height=12)
        self.tree.pack(side="left", fill="both", expand=True)
        
        scrollbar.config(command=self.tree.yview)
        self.tree.config(yscrollcommand=scrollbar.set)
        
        self.tree.heading("titulo", text="Título")
        self.tree.heading("fecha", text="Fecha y Hora")
        self.tree.heading("desc", text="Descripción")
        
        self.tree.column("titulo", width=150)
        self.tree.column("fecha", width=150)
        self.tree.column("desc", width=150)
        
        self.cargar_notificaciones()
        
        ttk.Button(self, text="Cerrar", command=self.on_closing).pack(pady=10)

    def cargar_notificaciones(self):
        tareas_pendientes = self.db.tareas_para_notificar()
        for tarea in tareas_pendientes:
            self.tree.insert("", "end", values=(tarea[1], tarea[3], tarea[2]))
        
        if not tareas_pendientes:
            self.tree.insert("", "end", values=("No hay notificaciones pendientes", "", ""))

    def verificar_notificaciones(self):
        while self.hilo_activo:
            tareas = self.db.listar_tareas()
            ahora = datetime.now()
            for t in tareas:
                id_tarea, titulo, desc, fecha_hora, notas, completada, categoria = t
                if completada:
                    continue
                try:
                    fecha_tarea = datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M")
                    diferencia = (fecha_tarea - ahora).total_seconds()
                    if 0 <= diferencia <= 60:
                        self.enviar_notificacion(titulo, notas or desc)
                        self.db.cursor.execute('UPDATE tareas SET notificada=1 WHERE id=?', (id_tarea,))
                        self.db.conn.commit()
                except Exception:
                    pass
            time.sleep(30)

    def enviar_notificacion(self, titulo, mensaje):
        notification.notify(
            title=f"⏰ Recordatorio: {titulo}",
            message=mensaje if mensaje else "Tienes una tarea pendiente.",
            timeout=10
        )

    def on_closing(self):
        self.hilo_activo = False
        self.destroy()