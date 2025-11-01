import tkinter as tk

def saludar():
    entrada2 = entrada.get()
    etiqueta.config(text= f"hola, {entrada2}!" )
    
ventana = tk.Tk()
ventana.title("Programa")
ventana.geometry("300x200") 


###Editar Ventana###
ventana.configure(
    bg="#494949",  # Color de fondo
    #lo mismo de geometry que está arriba:
    width=800,       # Ancho de la ventana
    height=600,      # Alto de la ventana
)
# Permitir redimensionar la ventana
ventana.resizable(True, True)  # (ancho, alto)

###Editar Etiqueta###



etiqueta= tk.Label(ventana,text="Holaaa")
etiqueta.pack()

entrada = tk.Entry(ventana)
entrada.pack()

boton = tk.Button(ventana, text = "Saludar", command = saludar)
boton.pack()

ventana.mainloop()



