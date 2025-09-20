import dearpygui.dearpygui as dpg
import sqlite3

DB_NAME = "mydatabase.db"


def create_table():
    cnx = sqlite3.connect(DB_NAME)
    c = cnx.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS personas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    edad INTEGER NOT NULL
                )''')
    cnx.commit()
    cnx.close()


def add_persona(nombre, apellido, edad):
    cnx = sqlite3.connect(DB_NAME)
    c = cnx.cursor()
    c.execute("INSERT INTO personas (nombre, apellido, edad) VALUES (?, ?, ?)", (nombre, apellido, edad))
    cnx.commit()
    cnx.close()

def get_personas():
    cnx = sqlite3.connect(DB_NAME)
    c = cnx.cursor()
    c.execute("SELECT * FROM personas")
    personas = c.fetchall()
    cnx.close()
    return personas

def update_persona(id, nombre, apellido, edad):
    cnx = sqlite3.connect(DB_NAME)
    c = cnx.cursor()
    c.execute("UPDATE personas SET nombre = ?, apellido = ?, edad = ? WHERE id = ?", (nombre, apellido, edad, id))
    cnx.commit()
    cnx.close()

def delete_persona(id):
    cnx = sqlite3.connect(DB_NAME)
    c = cnx.cursor()
    c.execute("DELETE FROM personas WHERE id = ?", (id,))
    cnx.commit()
    cnx.close()


def update_table():
    rows = dpg.get_item_children("tabla", 1)
    if rows:
        for row in rows:
            dpg.delete_item(row)
    for persona in get_personas():
        with dpg.table_row(parent="tabla"):
            dpg.add_text(str(persona[0]))
            dpg.add_text(persona[1])
            dpg.add_text(persona[2])
            dpg.add_text(str(persona[3]))


def guardar_persona():
    add_persona(dpg.get_value("nombre"), dpg.get_value("apellido"), int(dpg.get_value("edad")))
    update_table()

def modificar_persona():
    update_persona(int(dpg.get_value("id_mod")), dpg.get_value("nombre_mod"), dpg.get_value("apellido_mod"), int(dpg.get_value("edad_mod")))
    update_table()

def eliminar_persona():
    delete_persona(int(dpg.get_value("id_del")))
    update_table()


create_table()
dpg.create_context()
dpg.create_viewport(title="TP CRUD Personas", width=600, height=500)

with dpg.window(label="Gestión de Personas", width=580, height=480):
    dpg.add_text("Agregar Persona")
    dpg.add_input_text(label="Nombre", tag="nombre")
    dpg.add_input_text(label="Apellido", tag="apellido")
    dpg.add_input_text(label="Edad", tag="edad")
    dpg.add_button(label="Guardar", callback=guardar_persona)
    dpg.add_separator()

    dpg.add_text("Modificar Persona")
    dpg.add_input_text(label="ID", tag="id_mod")
    dpg.add_input_text(label="Nuevo Nombre", tag="nombre_mod")
    dpg.add_input_text(label="Nuevo Apellido", tag="apellido_mod")
    dpg.add_input_text(label="Nueva Edad", tag="edad_mod")
    dpg.add_button(label="Modificar", callback=modificar_persona)
    dpg.add_separator()

    dpg.add_text("Eliminar Persona")
    dpg.add_input_text(label="ID", tag="id_del")
    dpg.add_button(label="Eliminar", callback=eliminar_persona)
    dpg.add_separator()

    dpg.add_text("Personas registradas:")
    with dpg.table(header_row=True, tag="tabla"):
        dpg.add_table_column(label="ID")
        dpg.add_table_column(label="Nombre")
        dpg.add_table_column(label="Apellido")
        dpg.add_table_column(label="Edad")

dpg.setup_dearpygui()
dpg.show_viewport()
update_table()
dpg.start_dearpygui()
dpg.destroy_context()