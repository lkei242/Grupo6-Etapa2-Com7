import sqlite3

class BaseDatos:
    def __init__(self):
        self.conn = sqlite3.connect("organizador_tareas.db", check_same_thread=False) #crea (si no existe) o abre el archivo organizador_tareas.db
        self.cursor = self.conn.cursor()
        self.crear_tablas()
 
    def crear_tablas(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS categorias (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_categoria TEXT UNIQUE NOT NULL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            fecha_hora TEXT,
            notas TEXT,
            completada INTEGER DEFAULT 0,
            notificada INTEGER DEFAULT 0,
            categoria_id INTEGER,
            FOREIGN KEY(categoria_id) REFERENCES categorias(id_categoria)
        )
        ''')

        # Categorías iniciales
        categorias = ["Personal", "Trabajo", "Estudio", "Otros"]
        for c in categorias:
            self.cursor.execute("INSERT OR IGNORE INTO categorias(nombre_categoria) VALUES (?)", (c,))
        self.conn.commit()

    # CRUD de tareas
    # Listar todas las tareas, uniendo cada una con su categoría
    def listar_tareas(self):
        self.cursor.execute('''
            SELECT t.id, t.titulo, t.descripcion, t.fecha_hora, t.notas, t.completada, c.nombre_categoria
            FROM tareas t LEFT JOIN categorias c ON t.categoria_id = c.id_categoria
        ''')
        return self.cursor.fetchall()

    # Inserta una nueva fila en la tabla.
    def agregar_tarea(self, titulo, descripcion, fecha_hora, notas, categoria_id):
        self.cursor.execute('''
        INSERT INTO tareas (titulo, descripcion, fecha_hora, notas, categoria_id)
        VALUES (?, ?, ?, ?, ?)
        ''', (titulo, descripcion, fecha_hora, notas, categoria_id))
        self.conn.commit()

    # Modifica los valores de una tarea existente
    def actualizar_tarea(self, id, titulo, descripcion, fecha_hora, notas, categoria_id):
        self.cursor.execute('''
        UPDATE tareas SET titulo=?, descripcion=?, fecha_hora=?, notas=?, categoria_id=?
        WHERE id=?
        ''', (titulo, descripcion, fecha_hora, notas, categoria_id, id))
        self.conn.commit()

    # Elimina una tarea existente
    def eliminar_tarea(self, id):
        self.cursor.execute('DELETE FROM tareas WHERE id=?', (id,))
        self.conn.commit()

    # Marca como completada una tarea existente
    def marcar_completada(self, id):
        self.cursor.execute('UPDATE tareas SET completada=1 WHERE id=?', (id,))
        self.conn.commit()

    # Categorías
    # Lista todas las categorias
    def listar_categorias(self):
        self.cursor.execute("SELECT * FROM categorias ORDER BY nombre_categoria")
        return self.cursor.fetchall()

    def tareas_para_notificar(self):
        """
        Devuelve las tareas cuya fecha y hora ya pasó,
        y que todavía no fueron notificadas.
        """
        self.cursor.execute('''
            SELECT id, titulo, descripcion, fecha_hora
            FROM tareas
            WHERE completada = 0 AND notificada = 0
        ''')
        return self.cursor.fetchall()

    # Cerramos la conexion
    def cerrar(self):
        self.conn.close()
