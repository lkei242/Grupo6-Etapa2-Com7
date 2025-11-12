import threading
import time
from datetime import datetime
from plyer import notification # importacion de plyer para notificaciones del sistema operativo

class GestorNotificaciones:
    def __init__(self, db):
        self.db = db
        self.hilo_activo = True
        self.hilo = threading.Thread(target=self.verificar_notificaciones, daemon=True)
        self.hilo.start()

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

    def detener(self):
        self.hilo_activo = False
