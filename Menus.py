import tkinter as tk
from tkinter import ttk, messagebox
from BaseDatos import BaseDatos
from Formularios import FormularioTarea
import reloj_alarma #importando el reloj para agregarlo a las funciones del menu principal

###Menu perteneciente al Programa en sí###

class Menu:
    
    def __init__(self, ventana):
        self.ventana = ventana
        self.db = BaseDatos()   
        
    def menu_inicio (self):
        # Menú CRUD
        frame = ttk.Frame(self.ventana, padding=10)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="📋 Lista de Tareas", font=("Segoe UI", 14, "bold")).pack(pady=10)

        self.tree = ttk.Treeview(frame, columns=("desc", "fecha", "notas", "cat", "estado"), show="headings")
        for col, texto in zip(("desc", "fecha", "notas", "cat", "estado"), ["Descripción", "Fecha y Hora", "Notas", "Categoría", "Estado"]):
            self.tree.heading(col, text=texto)
            self.tree.column(col, width=150)
        self.tree.pack(fill="both", expand=True, pady=10)

        botones = ttk.Frame(frame)
        botones.pack(pady=5)

        ttk.Button(botones, text="➕ Nueva", command=self.nueva_tarea).grid(row=0, column=0, padx=5)
        ttk.Button(botones, text="✏️ Editar", command=self.editar_tarea).grid(row=0, column=1, padx=5)
        ttk.Button(botones, text="🗑️ Eliminar", command=self.eliminar_tarea).grid(row=0, column=2, padx=5)
        ttk.Button(botones, text="✅ Completar", command=self.completar_tarea).grid(row=0, column=3, padx=5)
        ttk.Button(botones, text="⏰ Abrir Reloj", command=self.abrir_reloj).grid(row=0, column=4, padx=5) #agrego boton del reloj
        

        self.actualizar_lista()
        
        #Crea el menú
        self.menu_horizontal = tk.Menu(self.ventana)
        #se lo asocia a la instancia de la ventana
        self.ventana.config(menu=self.menu_horizontal) 
        self.carga_menu1()
        self.carga_menu2()
        # Agregar el menu_ejemplo a la barra de menús
        #El add_cascade() sirve para agregar submenú a un menú principal
        self.menu_horizontal.add_cascade(label="Archivo", menu=self.menu_ejemplo) 
        # Agregar el menú 'Ayuda' a la barra de menús
        self.menu_horizontal.add_cascade(label="Ayuda", menu=self.menu_ejemplo2)
    
    # Refrescamos la tabla con las tareas actuales.
    def actualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for t in self.db.listar_tareas():
            estado = "✅" if t[5] else "❌"
            categoria = t[6] if t[6] else "Sin categoría"
            self.tree.insert("", "end", iid=t[0], values=(t[2], t[3], t[4], categoria, estado))

    # Abrimos un formulario vacío
    def nueva_tarea(self):
        form = FormularioTarea(self.ventana, self.db)
        self.ventana.wait_window(form)
        self.actualizar_lista()

    # Abrimos un formulario cargado con los datos seleccionados
    def editar_tarea(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Atención", "Selecciona una tarea.")
            return
        id = int(item[0])
        tarea = [t for t in self.db.listar_tareas() if t[0] == id][0]
        form = FormularioTarea(self.ventana, self.db, tarea)
        self.ventana.wait_window(form)
        self.actualizar_lista()

    # Elimina la tarea seleccionada (tras confirmar)
    def eliminar_tarea(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Atención", "Selecciona una tarea.")
            return
        id = int(item[0])
        if messagebox.askyesno("Confirmar", "¿Eliminar esta tarea?"):
            self.db.eliminar_tarea(id)
            self.actualizar_lista()

    # Marca la tarea como completada
    def completar_tarea(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Atención", "Selecciona una tarea.")
            return
        id = int(item[0])
        self.db.marcar_completada(id)
        self.actualizar_lista()



    ###Esto es para poblar los Menús###
    def carga_menu1(self):
        
        # El teroff=1 es para que se separen las opciones de la ventana, como una miniventana, caso contrario, tearoff=0, se queda donde está
        self.menu_ejemplo = tk.Menu(self.menu_horizontal, tearoff=0)
        self.menu_ejemplo.add_command(label="Menu 1", command=lambda: messagebox.showinfo("Título 1", "Opción 1"))
        self.menu_ejemplo.add_command(label="Menu 2", command=lambda: messagebox.showinfo("Título 2", "Opción 2"))
        self.menu_ejemplo.add_command(label="Menu 3", command=lambda: messagebox.showinfo("Título 3", "Opción 3"))
        self.menu_ejemplo.add_command(label="Menu 4", command=lambda: messagebox.showinfo("Título 4", "Opción 4"))
        self.menu_ejemplo.add_command(label="Menu 5", command=lambda: messagebox.showinfo("Título 5", "Opción 5"))
    
    def carga_menu2(self):
        # Hace lo mismo que lo anterior
        self.menu_ejemplo2 = tk.Menu(self.menu_horizontal, tearoff=0)
        self.menu_ejemplo2.add_command(label="Acerca de", command=lambda: messagebox.showinfo("Programa TPI", "Versión 1.0"))

    #Agreando la funcionalidad del reloj
    def abrir_reloj(self):
        #aca creamos una ventana secundaria tipo flotante para seguir viendo de fondo el menu
        self.ventana_reloj = tk.Toplevel(self.ventana)
        self.ventana_reloj.title("Reloj y Alarma")
        self.ventana_reloj.geometry("400x400")

        #Ahora va el contenido del reloj dentro de esa ventana
        reloj_frame = reloj_alarma.crear_reloj(self.ventana_reloj)
        reloj_frame.pack(expand= True, fill="both", pady=20)

        #Y agregamos la funcion de que vuelva al estado inicial cuando se oprima "volver al menu"
        btn_volver = tk.Button(self.ventana_reloj, text= "Volver al Menu", command=self.ventana_reloj.destroy)
        btn_volver.pack(pady=10)
