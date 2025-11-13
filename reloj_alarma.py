# reloj_alarma.py
"""
Módulo: reloj_alarma
Contiene una clase RelojAlarma que crea un Frame de Tkinter con:
 - reloj en vivo (HH:MM:SS)
 - entrada manual para fijar una hora de alarma (HH:MM:SS)
 - botones: Activar / Desactivar
 - aviso 1 minuto antes: "Chaque te queda un minuto"
 - aviso al momento: "¡Tiempo cumplido!"
"""

import tkinter as tk
from tkinter import messagebox
import time


def _parsear_hora_a_segundos(hora_texto):
    """Convierte 'HH:MM:SS' a segundos desde medianoche.
       Devuelve None si el formato es inválido."""
    try:
        parts = hora_texto.strip().split(":")
        if len(parts) != 3:
            return None
        h, m, s = map(int, parts)
        if not (0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59):
            return None
        return h * 3600 + m * 60 + s
    except Exception:
        return None


class RelojAlarma(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(bg=self.master.cget("bg"))
        self.alarm_active = False
        self.alarm_seconds = None
        self.warned_before = False  # para no repetir el aviso 1 minuto antes
        self.alarm_triggered = False

        # Widgets
        self.reloj_label = tk.Label(self, font=("Arial", 48), bg="black", fg="white")
        self.reloj_label.pack(pady=(10, 6))

        tk.Label(self, text="Ingresá la hora de la alarma (HH:MM:SS):",
                 bg="grey", fg="white", font=("Arial", 12)).pack(pady=(4, 2))

        self.entrada_alarma = tk.Entry(self, font=("Arial", 14), justify="center")
        self.entrada_alarma.pack(pady=4)

        botones_frame = tk.Frame(self, bg="grey")
        botones_frame.pack(pady=8)

        self.boton_activar = tk.Button(botones_frame, text="Activar alarma",
                                       command=self.activar_alarma, font=("Arial", 12),
                                       bg="lightgreen")
        self.boton_activar.grid(row=0, column=0, padx=8)

        self.boton_desactivar = tk.Button(botones_frame, text="Desactivar alarma",
                                          command=self.desactivar_alarma, font=("Arial", 12),
                                          bg="tomato")
        self.boton_desactivar.grid(row=0, column=1, padx=8)

        # Etiqueta pequeña para ver estado
        self.estado_label = tk.Label(self, text="Alarma: Inactiva", bg="black", fg="white",
                                     font=("Arial", 10))
        self.estado_label.pack(pady=(4, 10))

        # Iniciar el loop del reloj
        self._actualizar_reloj()

    def _actualizar_reloj(self):
        ahora = time.localtime()
        texto = time.strftime("%H:%M:%S", ahora)
        self.reloj_label.config(text=texto)
        self._verificar_alarma(ahora)
        # repetir cada 1000 ms (1 segundo)
        self.after(1000, self._actualizar_reloj)

    def _verificar_alarma(self, ahora_struct):
        if not self.alarm_active or self.alarm_seconds is None:
            return

        ahora_seg = ahora_struct.tm_hour * 3600 + ahora_struct.tm_min * 60 + ahora_struct.tm_sec
        # normalizamos dentro de 0..86399 (por si hay desbordes)
        ahora_seg = ahora_seg % 86400
        alarma = self.alarm_seconds % 86400

        # 1) aviso 1 minuto antes (solo una vez)
        if ahora_seg == (alarma - 60) % 86400 and not self.warned_before:
            self.warned_before = True
            messagebox.showinfo("Aviso", "Chaque te queda 1 minuto 😱⏰")

        # 2) aviso en el momento exacto (solo una vez)
        if ahora_seg == alarma and not self.alarm_triggered:
            self.alarm_triggered = True
            messagebox.showwarning("Tiempo cumplido! 💪⏰")
            # Después de disparar, desactivamos la alarma para que no se repita
            self.desactivar_alarma()

    def activar_alarma(self):
        texto = self.entrada_alarma.get().strip()
        seg = _parsear_hora_a_segundos(texto)
        if seg is None:
            messagebox.showwarning("Error", "Por favor ingresá una hora válida (formato HH:MM:SS).")
            return
        self.alarm_seconds = seg
        self.alarm_active = True
        self.warned_before = False
        self.alarm_triggered = False
        self.estado_label.config(text=f"Alarma: Activa → {texto}")

        messagebox.showinfo("Alarma activada", f"Alarma fijada para las {texto} ⏰")

    def desactivar_alarma(self):
        self.alarm_active = False
        self.alarm_seconds = None
        self.warned_before = False
        self.alarm_triggered = False
        self.estado_label.config(text="Alarma: Inactiva")
        messagebox.showinfo("Alarma desactivada", "La alarma fue cancelada, ñeri.")


# --- Función helper para crear e integrar el widget en la app principal ---
def crear_reloj(master=None):
    """Crea y devuelve el Frame con el reloj"""
    frame = RelojAlarma(master)
    return frame


# --- Permitir ejecución directa para testear el módulo ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Reloj con Alarma Chaqueña (prueba)")
    root.geometry("500x320")
    root.config(bg="black")
    reloj_frame = crear_reloj(root)
    reloj_frame.pack(expand=True, fill="both", padx=10, pady=10)
    root.mainloop()