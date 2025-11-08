import sqlite3

# **************************
# BASE DE DATOS
# **************************
conn = sqlite3.connect('organizador_tareas.db', check_same_thread=False)
cursor = conn.cursor()

# Crear tabla de categorías
cursor.execute('''
CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_categoria TEXT UNIQUE NOT NULL
)
''')

# Crear tabla de tareas con categoría
cursor.execute('''
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

conn.commit()

# Categorías por defecto
categorias_por_defecto = ["Personal", "Trabajo", "Estudio", "Otros"]

for cat in categorias_por_defecto:
    cursor.execute("INSERT OR IGNORE INTO categorias(nombre_categoria) VALUES (?)", (cat,))

conn.commit()