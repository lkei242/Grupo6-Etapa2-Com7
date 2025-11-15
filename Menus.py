import tkinter as tk
from tkinter import ttk, messagebox
from Formularios import FormularioTarea
import reloj_alarma #importando el reloj para agregarlo a las funciones del menu principal

class Menu:
    
    def __init__(self, ventana, db, temas, tema_actual, cambiar_tema_callback):
        self.ventana = ventana
        self.db = db
        self.temas = temas
        self.tema_actual = tema_actual
        self.cambiar_tema_callback = cambiar_tema_callback
        self.colores = temas[tema_actual]
        self.ventana_notif = None
        self.configurar_estilo()
        
    def configurar_estilo(self):
        self.estilo = ttk.Style()
        self.estilo.theme_use('clam')
        
        self.estilo.configure('TFrame', background=self.colores["bg_principal"])
        self.estilo.configure('TLabel', background=self.colores["bg_principal"], foreground=self.colores["fg_texto"])
        self.estilo.configure('TButton', background=self.colores["bg_secundario"], foreground=self.colores["fg_texto"])
        self.estilo.configure('Treeview', background=self.colores["bg_secundario"], foreground=self.colores["fg_texto"], fieldbackground=self.colores["bg_secundario"], borderwidth=0)
        self.estilo.configure('Treeview.Heading', background=self.colores["border"], foreground=self.colores["fg_texto"])
        self.estilo.map('TButton', background=[('active', self.colores["fg_acento"])])
        
    def menu_inicio(self):
        # Limpiar widgets anteriores
        for widget in self.ventana.winfo_children(): #itera sobre todos los widgets hijos
            if isinstance(widget, ttk.Frame): #y si el widget es un Frame elimina
                widget.destroy()

        frame = ttk.Frame(self.ventana, padding=10)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="📋 Lista de Tareas", font=("Segoe UI", 14, "bold")).pack(pady=10)
        botones = ttk.Frame(frame)
        botones.pack(pady=5)
        ttk.Button(botones, text="🔔 Notificaciones", command=self.ver_notificaciones).grid(row=0, column=4, padx=5)

        tree_container = ttk.Frame(frame)
        tree_container.pack(fill="both", expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_container, orient="vertical")
        self.tree = ttk.Treeview(tree_container, columns=("desc", "fecha", "notas", "cat", "estado"), show="headings")
        
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
        self.tree.config(yscrollcommand=scrollbar.set)

        for col, texto in zip(("desc", "fecha", "notas", "cat", "estado"), ["Descripción", "Fecha y Hora", "Notas", "Categoría", "Estado"]):
            self.tree.heading(col, text=texto)
            self.tree.column(col, width=150)

        botones = ttk.Frame(frame)
        botones.pack(pady=5)

        ttk.Button(botones, text="➕ Nueva", command=self.nueva_tarea).grid(row=0, column=0, padx=5)
        ttk.Button(botones, text="✏️ Editar", command=self.editar_tarea).grid(row=0, column=1, padx=5)
        ttk.Button(botones, text="🗑️ Eliminar", command=self.eliminar_tarea).grid(row=0, column=2, padx=5)
        ttk.Button(botones, text="✅ Completar", command=self.completar_tarea).grid(row=0, column=3, padx=5)
        ttk.Button(botones, text="⏰ Abrir Reloj", command=self.abrir_reloj).grid(row=0, column=4, padx=5) #agrego boton del reloj
                
        self.actualizar_lista()
        
        # Crea el menú
        self.menu_horizontal = tk.Menu(self.ventana, bg=self.colores["bg_secundario"], fg=self.colores["fg_texto"])
        self.ventana.config(menu=self.menu_horizontal) 
        self.carga_Menu()
        self.carga_menu_ayuda()
        self.menu_horizontal.add_cascade(label="Tema", menu=self.Menu) 
        self.menu_horizontal.add_cascade(label="Ayuda", menu=self.menu_ayuda)
    
    def actualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for t in self.db.listar_tareas():
            estado = "✅" if t[5] else "❌"
            categoria = t[6] if t[6] else "Sin categoría"
            self.tree.insert("", "end", iid=t[0], values=(t[2], t[3], t[4], categoria, estado))

    def nueva_tarea(self):
        form = FormularioTarea(self.ventana, self.db, self.colores)
        self.ventana.wait_window(form)
        self.actualizar_lista()

    def editar_tarea(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Atención", "Selecciona una tarea.")
            return
        id = int(item[0])
        tarea = [t for t in self.db.listar_tareas() if t[0] == id][0]
        form = FormularioTarea(self.ventana, self.db, self.colores, tarea)
        self.ventana.wait_window(form)
        self.actualizar_lista()

    def eliminar_tarea(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Atención", "Selecciona una tarea.")
            return
        id = int(item[0])
        if messagebox.askyesno("Confirmar", "¿Eliminar esta tarea?"):
            self.db.eliminar_tarea(id)
            self.actualizar_lista()

    def completar_tarea(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Atención", "Selecciona una tarea.")
            return
        id = int(item[0])
        self.db.marcar_completada(id)
        self.actualizar_lista()

    def ver_notificaciones(self):
        from Notificaciones import VentanaNotificaciones
        # Verifica si ya existe una ventana de notificaciones abierta
        if self.ventana_notif and self.ventana_notif.winfo_exists():
            self.ventana_notif.lift()  # Trae la ventana al frente
            return
        # Verifica si hay notificaciones
        tareas_pendientes = self.db.tareas_para_notificar()
        if not tareas_pendientes:
            messagebox.showinfo("Notificaciones", "No hay notificaciones pendientes.")
            return
        
        
        self.ventana_notif = VentanaNotificaciones(self.ventana, self.db, self.colores)
        self.ventana.wait_window(self.ventana_notif)
        self.ventana_notif = None

    def carga_Menu(self):
        self.Menu = tk.Menu(self.menu_horizontal, tearoff=0, bg=self.colores["bg_secundario"], fg=self.colores["fg_texto"], activebackground=self.colores["fg_acento"])
        self.Menu.add_command(label="🌙 Modo Oscuro", command=lambda: self.cambiar_tema_callback("oscuro"))
        self.Menu.add_command(label="☀️ Modo Claro", command=lambda: self.cambiar_tema_callback("claro"))
        self.Menu.add_command(label="Borrar todas las tareas", command=self.borrar_todas_tareas)
    
    def borrar_todas_tareas(self):
        tareas = self.db.listar_tareas()
        if not tareas:
            messagebox.showinfo("Sin tareas", "Sin tareas")
            return
        
        if messagebox.askyesno("Confirmar", "¿Eliminar todas las tareas? Esta acción no se puede deshacer."):
            for tarea in tareas:
                self.db.eliminar_tarea(tarea[0])
            self.actualizar_lista()
            messagebox.showinfo("Éxito", "Todas las tareas han sido eliminadas.")
    
    def carga_menu_ayuda(self):
        self.menu_ayuda = tk.Menu(self.menu_horizontal, tearoff=0, bg=self.colores["bg_secundario"], fg=self.colores["fg_texto"], activebackground=self.colores["fg_acento"])
        self.menu_ayuda.add_command(label="Acerca de", command=lambda: messagebox.showinfo("Detalles", "Organizador de Tareas.\nVersión 1.0"))
    
    
        #Agreando la funcionalidad del reloj
    def abrir_reloj(self):
        # aca creamos una ventana secundaria tipo flotante para seguir viendo de fondo el menu
        self.ventana_reloj = tk.Toplevel(self.ventana)
        self.ventana_reloj.title("Reloj y Alarma")
        self.ventana_reloj.geometry("400x400")
        # aplicar fondo del tema a la ventana del reloj
        self.ventana_reloj.config(bg=self.colores["bg_principal"])

        # Ahora va el contenido del reloj dentro de esa ventana (pasamos colores)
        reloj_frame = reloj_alarma.crear_reloj(self.ventana_reloj, self.colores)
        reloj_frame.pack(expand=True, fill="both", pady=20)

        # Y agregamos la funcion de que vuelva al estado inicial cuando se oprima "volver al menu"
        btn_volver = tk.Button(self.ventana_reloj, text="Volver al Menu",command=self.ventana_reloj.destroy, bg=self.colores["bg_secundario"],fg=self.colores["fg_texto"],activebackground=self.colores["fg_acento"])
        btn_volver.pack(pady=10)    