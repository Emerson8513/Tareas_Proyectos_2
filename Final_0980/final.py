import psycopg2
import os
import qrcode
import time
import cv2
from pyzbar import pyzbar
import numpy as np
import ast 
import pandas as pd
import matplotlib.pyplot as plt
import re
from unicodedata import normalize

conn = psycopg2.connect(
    dbname="Final",
    user="emerson",
    password="kuto",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

def crear_tabla(usuario):
    # Asegúrate de que el nombre de la tabla sea seguro para usar en SQL
    usuario = re.sub(r'\W+', '', usuario)  # Elimina caracteres no alfanuméricos

    create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {usuario} (
        Usuario VARCHAR(50),
        opcion VARCHAR(50),
        fecha TIMESTAMP,
        comprobar VARCHAR(50),
        resultado VARCHAR(50)
    );
    '''
    cursor.execute(create_table_query)
    conn.commit()

def es_palindromo(cadena):
    """Determina si una cadena es un palíndromo."""
    return cadena == cadena[::-1]

def solicitar_numero_primo(mensaje):
    while True:
        entrada = input(mensaje)
        if entrada.isdigit():  
            numero = int(entrada)
            if numero > 0:  
                return numero
            else:
                print("Error: El número debe ser mayor que cero.")
        else:
            print("Error: Solo se permiten números enteros positivos.")
    
def solicitar_mensaje_string(mensaje):
    while True:
        entrada = input(mensaje)
        entrada = re.sub(
            r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
            normalize("NFD", entrada), 0, re.I
        )
        entrada = normalize('NFC', entrada)
        entrada = entrada.replace(" ", "")
        entrada = entrada.replace(",", "")
        entrada = entrada.replace(".", "")
        entrada = entrada.lower()
        print(entrada)
        return entrada

def info_usuario(usuario, opcion, fecha, comprobar, resultado):
    cursor.execute(f"INSERT INTO {usuario} (Usuario, fecha, opcion, comprobar, resultado) VALUES (%s, %s, %s, %s, %s);", (usuario, fecha, opcion, comprobar, resultado))
    conn.commit()

def menu():
    print("1. Ingresar usuario")
    print("2. Ejecutar Programa")
    print("3. Historial de usuario")
    print("4. Borrar Datos")
    print("5. Salir")

def menu_ejecutar():
    print("1. Verificar si un número es perfecto.")
    print("2. Verificar si un número es primo.")
    print("3. Verificar si una cadena es palíndromo.")
    print("4. Salir")

opcion = 0
opcion_ejecutar = 0
directorio_txt = "/home/emerson/Documentos/Tareas_Proyectos_2/Final_0980/Archivos_TXT/"
date_time = time.strftime("%m/%d/%Y, %H:%M:%S")


while opcion != 5:
    menu()
    
    opcion = solicitar_numero_primo("Seleccione una opción: ")
    if opcion > 5:
        print("Error: Seleccione una opción válida.\n Ingrese un Numero menor a 6")
        continue

    if opcion == 1:
        usuario = solicitar_mensaje_string("Ingrese su nombre de usuario: ")
        crear_tabla(usuario)
        comprobar = "None"
        resultado = "None"
        opcion_s = "Primer Ingreso"
        date_time = time.strftime("%m/%d/%Y, %H:%M:%S")
        print("Tabla creada correctamente.")
        info_usuario(usuario, opcion_s, date_time, comprobar, resultado)
        print("Datos ingresados correctamente.")

    if opcion == 2:
        print("USTED ELIGIO LA OPCION DE EJECUTAR PROGRAMA")
        while opcion_ejecutar != 4:      
            menu_ejecutar()
            opcion_ejecutar = solicitar_numero_primo("Seleccione una opción: ")
            
            if opcion_ejecutar > 4:
            
                print("    Error: Seleccione una opción válida.")
                print("    Ingrese un número menor a 5.")
                continue
                
            if opcion_ejecutar == 1:
                print("USTED ELIGIO LA OPCION DE VERIFICAR SI UN NUMERO ES PERFECTO")
                opcion_s = "Verificar si un número es perfecto."
                usuario = solicitar_mensaje_string("Ingrese su nombre de usuario: ")
                perfecto = solicitar_numero_primo("Ingrese un número: ")
                suma_divisores = 0
                
                for i in range(1, perfecto):
                    if perfecto % i == 0:
                        suma_divisores += i
                print(f"Usuario: {usuario}")
                print(f"Operación: {opcion_s}")
                print(f"Número ingresado: {perfecto}")
                
                if suma_divisores == perfecto:
                    print("Resultado: El número es perfecto.")
                    resultado = "Es perfecto"
                else:
                    print("Resultado: El número no es perfecto.")
                    resultado = "No es perfecto"
                
                comprobar = perfecto
                info_usuario(usuario, opcion_s, date_time, comprobar, resultado)

            if opcion_ejecutar == 2:
                print("USTED ELIGIO LA OPCION DE VERIFICAR SI UN NUMERO ES PRIMO")
                opcion_s = "Verificar si un número es primo"
                usuario = solicitar_mensaje_string("Ingrese su nombre de usuario: ")
                primo = solicitar_numero_primo("Ingrese un número: ")                
                
                print(f"Usuario: {usuario}")
                print(f"Operación: {opcion_s}")
                print(f"Número ingresado: {primo}")
                
                if primo <= 1:
                    print("Resultado: El número debe ser mayor que 1.")
                    resultado = "No válido"
                else:
                    for i in range(2, int(primo**0.5) + 1):
                        if primo % i == 0:
                            print("Resultado: El número no es primo.")
                            resultado = "No es primo"
                            break
                    else:
                        print("Resultado: El número es primo.")
                        resultado = "Es primo"
                
                print("="*10 + "\n")
                comprobar = primo
                info_usuario(usuario, opcion_s, date_time, comprobar, resultado)
            
            if opcion_ejecutar == 3:
                print("USTED ELIGIO LA OPCION DE VERIFICAR SI UNA CADENA ES PALINDROMO")
                opcion_s = "Verificar si una cadena es palíndromo."
                usuario = solicitar_mensaje_string("Ingrese su nombre de usuario: ")
                cadena = solicitar_mensaje_string("Ingrese una cadena: ")
                
                print("\n" + "="*40)
                print(f"Usuario: {usuario}")
                print(f"Operación: {opcion_s}")
                print(f"Cadena ingresada: {cadena}")
                
                if es_palindromo(cadena):
                    print("Resultado: La cadena es palíndromo.")
                    resultado = "Es palíndromo"
                else:
                    print("Resultado: La cadena no es palíndromo.")  
                    resultado = "No es palíndromo"   
                
                print("="*40 + "\n")
                comprobar = cadena            
                info_usuario(usuario, opcion_s, date_time, comprobar, resultado)
    if opcion == 3:
        print("USTED ELIGIO LA OPCION DE HISTORIAL DE DATOS")
        cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
        tablas = cursor.fetchall()  # Imprimir el listado de tablas
        print("Usuario Disponibles:")
        for tabla in tablas:
            print(tabla[0])
        usuario = solicitar_mensaje_string("Ingrese su nombre de usuario: ")
        cursor.execute(f"SELECT * FROM {usuario};")
        registros = cursor.fetchall()
        df = pd.DataFrame(registros, columns=["Usuario", "Fecha", "Opción", "Comprobar", "Resultado"])
        print(df)
        df.to_csv(f"{directorio_txt}{usuario}.txt", index=False)
        print(f"Datos exportados correctamente de {usuario}.")
    if opcion == 4:
        print("USTED ELIGIO LA OPCION DE BORRAR DATOS")
        cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
        tablas = cursor.fetchall()  # Imprimir el listado de tablas
        print("Usuario Disponibles:")
        for tabla in tablas:
            print(tabla[0])
        usuario = solicitar_mensaje_string("Ingrese su nombre de usuario a borrar: ")
        cursor.execute(f"DROP TABLE {usuario};")
        conn.commit()
        print(f"Datos eliminados correctamente de {usuario}.")
    if opcion == 5:
        print("Saliendo del programa...")
        break

cursor.close()
conn.close()
