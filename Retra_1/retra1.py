import psycopg2
import os
import datetime
import time
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


conn = psycopg2.connect(
    dbname="Retra1",
    user="emerson",
    password="kuto",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

create_table_query = '''
    CREATE TABLE IF NOT EXISTS bitacora (
        usuario VARCHAR(255)  NULL,
        fecha VARCHAR(50),
        hora VARCHAR(50),
        accion VARCHAR(255)  NULL
    );
'''
cursor.execute(create_table_query)
conn.commit()
def crear_tabla(usuario):
    # Asegúrate de que el nombre de la tabla sea seguro para usar en SQL
    usuario = re.sub(r'\W+', '', usuario)  # Elimina caracteres no alfanuméricos
    create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {usuario} (
        usuario VARCHAR(50),
        tarea VARCHAR(50),
        fecha VARCHAR(50),
        hora VARCHAR(50),
        accion VARCHAR(50)
    );
    '''
    cursor.execute(create_table_query)
    conn.commit()


def menu():
    print("QUE DESEA REALIZAR")
    print("1. Ingresar Informacion de Usuario")
    print("2. Ejecutar Programa")
    print("3. Borrar Información")
    print("4. Historial de Usuarios")
    print("5. Salir")

def menu_usuario():
    print("1. Agregar Tarea")
    print("2. Modificar Tarea")
    print("3. Eliminar Tarea")
    print("4. Ver Tareas")
    print("5. Salir")

def ingresar_entero_tarea(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            if valor > 0 and valor < 5:
                return valor
            else:
                print("El valor debe ser positivo")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero positivo entre 1 y 4.")

def ingresar_entero_positivo(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            if valor > 0 and valor < 6:
                return valor
            else:
                print("El valor debe ser positivo entre 1 y 5.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero positivo entre 1 y 5.")

def ingresar_string(mensaje):
    while True:
        try:
            valor = str(input(mensaje))
            if valor.isalpha():
                return valor
            else:
                print("El valor debe ser una cadena de caracteres.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un string.")

def ingresar_entero_borrar(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            if valor > 0 and valor < 4:
                return valor
            else:
                print("El valor debe ser positivo")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero positivo entre 1 y 3.")

def hora_ejecucion():
    hora = datetime.datetime.now().strftime("%H:%M:%S")
    return hora
def fecha_ejecucion():
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    return fecha

def borrar_tabla(usuario):
    # Sanitize table name
    usuario = re.sub(r'\W+', '', usuario)
    drop_table_query = f'DROP TABLE IF EXISTS {usuario};'
    cursor.execute(drop_table_query)
    conn.commit()

def historial_usuario(usuario):
    # Sanitize table name
    usuario = re.sub(r'\W+', '', usuario)
    try:
        cursor.execute(f"SELECT * FROM {usuario}")
        registros = cursor.fetchall()
        if registros:
            for registro in registros:
                print(registro)
        else:
            print("No hay registros para este usuario")
    except psycopg2.Error as e:
        print(f"Error al consultar el historial: {e}")

def agregar_tarea(usuario,user, tarea, fecha, hora, accion):
    insert_query = f"INSERT INTO {usuario} (usuario, tarea, fecha, hora, accion) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (user, tarea, fecha, hora, accion))
    conn.commit()
    with open(f"{archivos_txt}/{user}.txt", "a") as archivo:
        archivo.write(f"{tarea} - {fecha} - {hora} - {accion}\n")

def modificar_tarea(usuario, tarea, fecha, hora, accion):
    update_query = f"UPDATE {usuario} SET tarea = %s, fecha = %s, hora = %s, accion = %s WHERE tarea = %s"
    cursor.execute(update_query, (tarea, fecha, hora, accion, tarea))
    conn.commit()

def eliminar_tarea(usuario, tarea):
    delete_query = f"DELETE FROM {usuario} WHERE tarea = %s"
    cursor.execute(delete_query, (tarea,))
    conn.commit()

def ver_tareas(usuario):
    cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema='public'""")
    tables = cursor.fetchall()
    for table in tables:
        print(table[0])
    usuario = ingresar_string("Ingrese el nombre de la tabla: ")
    select_query = f"SELECT * FROM {usuario}"
    cursor.execute(select_query)
    historial = cursor.fetchall()
    print(historial)
    return cursor.fetchall()    

    
#usuario = ingresar_string("Ingrese su nombre de usuario: ")
#crear_tabla(usuario)
pruebaf = fecha_ejecucion()
print(f"La fecha de ejecución es: {pruebaf}")
prueba = hora_ejecucion()
print(f"La hora de ejecución es: {prueba}")

opcion = 0
archivos_txt = "/home/emerson/Documentos/Tareas_Proyectos_2/Retra_1/Archivos_txt"

if not os.path.exists(archivos_txt):
    os.makedirs(archivos_txt)
    print(f"El directorio {archivos_txt} ha sido creado.")
else:
    print(f"El directorio {archivos_txt} ya existe.")

while opcion != 5:
    menu()
    opcion = ingresar_entero_positivo("Ingrese una opción: ")

    if opcion == 1:
        print("Ingrese su nombre de usuario: ")
        usuario = ingresar_string("Ingrese su nombre de usuario: ")
        crear_tabla(usuario)
    if opcion == 2:
        menu_usuario()
        opcion_usuario = ingresar_entero_tarea("Ingrese una opción: ")
        if opcion_usuario == 1:

            usuario = ingresar_string("Ingrese su nombre de usuario: ")
            user = usuario
            tarea = input("Ingrese la tarea: ")
            fecha = fecha_ejecucion()
            hora = hora_ejecucion()
            accion = "Agregar"
            agregar_tarea(usuario,user, tarea, fecha, hora, accion)

        if opcion_usuario == 2:
            usuario = ingresar_string("Ingrese su nombre de usuario: ")
            user = usuario

            tarea = input("Ingrese la tarea: ")
            fecha = fecha_ejecucion()
            hora = hora_ejecucion()
            accion = "Modificar"
            modificar_tarea(usuario, user,tarea, fecha, hora, accion)
        if opcion_usuario == 3:
            tarea = input("Ingrese la tarea: ")
            fecha = fecha_ejecucion()
            hora = hora_ejecucion()
            accion = "Eliminar"
            eliminar_tarea(usuario,user, tarea, fecha, hora, accion)
        if opcion_usuario == 4:
            ver_tareas(usuario)
        if opcion_usuario == 5:
            break

    if opcion == 3:
        print("Ingrese su nombre de usuario: ")
        usuario = ingresar_string("Ingrese su nombre de usuario: ")
        borrar_tabla(usuario)
    if opcion == 4:
        print("Ingrese su nombre de usuario: ")
        usuario = ingresar_string("Ingrese su nombre de usuario: ")
        historial_usuario(usuario)
    if opcion == 5:
        print("Saliendo del programa...")
        break

    


cursor.close()
conn.close()
