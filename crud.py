import sqlite3
from tkinter import messagebox
from base_datos import conn, cursor

# **************************
# CRUD ORGANIZADOR DE TAREAS
# **************************

# Categorias
# Crear una categoria
def crear_categoria(nombre):
    try:
        cursor.execute("INSERT INTO categorias(nombre_categoria) VALUES (?)", (nombre,))
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "La categoría ya existe.")

# Listar categorias
def obtener_categorias():
    cursor.execute("SELECT * FROM categorias ORDER BY nombre_categoria")
    return cursor.fetchall()

# Editar categoria
def editar_categoria(id_categoria, nuevo_nombre):
    try:
        cursor.execute("UPDATE categorias SET nombre_categoria=? WHERE id_categoria=?", (nuevo_nombre, id_categoria))
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Ya existe una categoría con ese nombre.")

# Eliminar categoria
def eliminar_categoria(id_categoria):
    cursor.execute("SELECT COUNT(*) FROM tareas WHERE categoria_id=?", (id_categoria,))
    count = cursor.fetchone()[0]
    if count > 0:
        messagebox.showwarning("Advertencia", "No puedes eliminar una categoría que tiene tareas asociadas.")
        return
    cursor.execute("DELETE FROM categorias WHERE id_categoria=?", (id_categoria,))
    conn.commit()