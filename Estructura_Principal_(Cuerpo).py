import tkinter as tk
from tkinter import messagebox

    
ventana = tk.Tk()
ventana.title("Programa")
#ventana.geometry("300x200") 


###Editar Ventana###
ventana.configure(
    bg="#494949",  # Color de fondo de la ventana
    #lo mismo de geometry que está arriba:
    width=800,       # Ancho de la ventana
    height=600,      # Alto de la ventana
)
# El usuario puede redimensionar la ventana con esto:
ventana.resizable(True, True)  # (ancho, alto)

###Menu del Programa en sí###

menu_horizontal = tk.Menu(ventana) #Crea el menú
ventana.config(menu=menu_horizontal) #se lo asocia a la instancia de la ventana

###Esto es para crear los Menús###
# El teroff=1 es para que se separen las opciones de la ventana, como una miniventana, caso contrario, tearoff=0, se queda donde está
menu_ejemplo = tk.Menu(menu_horizontal, tearoff=0)
menu_ejemplo.add_command(label="Menu 1", command=lambda: messagebox.showinfo("Título 1", "Opción 1"))
menu_ejemplo.add_command(label="Menu 2", command=lambda: messagebox.showinfo("Título 2", "Opción 2"))
menu_ejemplo.add_command(label="Menu 3", command=lambda: messagebox.showinfo("Título 3", "Opción 3"))
menu_ejemplo.add_command(label="Menu 4", command=lambda: messagebox.showinfo("Título 4", "Opción 4"))
menu_ejemplo.add_command(label="Menu 5", command=lambda: messagebox.showinfo("Título 5", "Opción 5"))


# Agregar el menu_ejemplo a la barra de menús
menu_horizontal.add_cascade(label="Archivo", menu=menu_ejemplo) #El add_cascade() sirve para agregar submenú a un menú principal

# Hace lo mismo que lo anterior
menu_ejemplo2 = tk.Menu(menu_horizontal, tearoff=0)
menu_ejemplo2.add_command(label="Acerca de", command=lambda: messagebox.showinfo("Programa TPI", "Versión 1.0"))

# Agregar el menú 'Ayuda' a la barra de menús
menu_horizontal.add_cascade(label="Ayuda", menu=menu_ejemplo2)

#Esto inicia la ventana y la va actualizando todo el rato
ventana.mainloop()




