import tkinter as tk
from tkinter import messagebox

###Menu perteneciente al Programa en sí###

class Menu:
    
    def __init__(self, ventana):
        self.ventana = ventana
        
    def menu_inicio (self):
        self.menu_horizontal = tk.Menu(self.ventana) #Crea el menú
        self.ventana.config(menu=self.menu_horizontal) #se lo asocia a la instancia de la ventana
        self.carga_menu1()
        self.carga_menu2()
        # Agregar el menu_ejemplo a la barra de menús
        self.menu_horizontal.add_cascade(label="Archivo", menu=self.menu_ejemplo) #El add_cascade() sirve para agregar submenú a un menú principal
        # Agregar el menú 'Ayuda' a la barra de menús
        self.menu_horizontal.add_cascade(label="Ayuda", menu=self.menu_ejemplo2)
        
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

