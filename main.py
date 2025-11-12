import tkinter as tk
from Menus import Menu
from BaseDatos import BaseDatos
from Notificaciones import GestorNotificaciones 

class Ventana:
    def __init__(self):
        self.ventana = tk.Tk()
        self.db = BaseDatos()  
        self.notificaciones = GestorNotificaciones(self.db)

    def iniciar(self):
        self.ventana.title("🕒 Organizador de Tareas")
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


if __name__ == "__main__": #Ejecuta el código que sigue solo si este archivo es el que el usuario está corriendo directamente
    ventana = Ventana()
    ventana.iniciar()

