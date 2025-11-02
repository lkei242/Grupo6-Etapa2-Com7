import tkinter as tk
from Menus import Menu


class Ventana:
    def __init__(self):
        self.ventana = tk.Tk()

    def iniciar(self):
        self.ventana.title("Programa")
        self.config_Default()
        self.mostrar_Menu()
        self.ventana.mainloop()
        
    #Configura por default
    def config_Default(self):
        
        self.ventana.configure(
        bg="#494949",  # Color de fondo de la ventana
        #lo mismo que geometry:
        width=800,       # Ancho 
        height=600,      # Alto
        )
        # El usuario puede redimensionar la ventana con esto:
        self.ventana.resizable(True, True)  # (ancho, alto)
    
    def mostrar_Menu(self):
        self.menu = Menu(self.ventana)
        self.menu.menu_inicio()


ventana = Ventana()
ventana.iniciar()

