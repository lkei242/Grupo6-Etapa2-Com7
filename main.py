import tkinter as tk
from Menus import Menu
from BaseDatos import BaseDatos
from Notificaciones import VentanaNotificaciones 

# Diccionario con los colores del tema:
TEMAS = {
    "oscuro": {
        "bg_principal": "#1e1e1e",
        "bg_secundario": "#2d2d2d",
        "fg_texto": "#ffffff",
        "fg_acento": "#64b5f6",
        "border": "#3d3d3d"
    },
    "claro": {
        "bg_principal": "#ffffff",
        "bg_secundario": "#f0f0f0",
        "fg_texto": "#000000",
        "fg_acento": "#0078d4",
        "border": "#e0e0e0"
    }
}

class Ventana:
    def __init__(self):
        self.ventana = tk.Tk()
        self.db = BaseDatos()  
        self.tema_actual = "oscuro"  # Tema por defecto
        
        

    def iniciar(self):
        self.ventana.title("🕒 Organizador de Tareas")
        self.config_Default()
        self.mostrar_Menu()
        self.ventana.mainloop()
        
    def config_Default(self):
        colores = TEMAS[self.tema_actual]
        self.ventana.configure(
            bg=colores["bg_principal"],
            width=800,
            height=600,
        )
        self.ventana.resizable(True, True)
    
    def cambiar_tema(self, nuevo_tema):
        self.tema_actual = nuevo_tema
        colores = TEMAS[self.tema_actual]
        self.ventana.configure(bg=colores["bg_principal"])
        # Recargar el menú con el nuevo tema
        self.mostrar_Menu()
    
    def mostrar_Menu(self):
        self.menu = Menu(self.ventana, self.db, TEMAS, self.tema_actual, self.cambiar_tema) #Paso la función como referencia 🔗
        self.menu.menu_inicio()


if __name__ == "__main__":
    ventana = Ventana()
    ventana.iniciar()