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

conn = psycopg2.connect(
    dbname="parqueo",
    user="postgres",
    password="kuto",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

create_table_query = '''
    CREATE TABLE IF NOT EXISTS parqueo (
    Usuario VARCHAR(50),
    nit int NOT NULL,
    placa VARCHAR(50),
    hora_entrada int NOT NULL,
    minutos_entrada int NOT NULL,
    hora_salida int NOT NULL,
    minutos_salida int NOT NULL
);
'''

cursor.execute(create_table_query)
conn.commit()

def info_usuario(user, nit, placa, hora_in, minutos_in, hora_out, minutos_out):
    print("Bienvenido al Parqueo El COLOCHO")
    cursor.execute("INSERT INTO parqueo (Usuario, nit, placa, hora_entrada, minutos_entrada, hora_salida, minutos_salida) VALUES (%s, %s, %s, %s,%s, %s,%s);", (user, nit, placa, hora_in, minutos_in, hora_out, minutos_out))
    conn.commit()

def menu():
    print("QUE DESEA REALIZAR")
    print("1. Ingresar Informacion de Usuario")
    print("2. Ejecutar Programa")
    print("3. Borrar Información")
    print("4. Historial de Usuarios")
    print("5. Salir")

def historial():
    cursor.execute("SELECT * FROM parqueo;")
    rows = cursor.fetchall()
    for row in rows:
        print(f"Usuario: {row[0]}, Placa: {row[2]}, Nit: {row[1]}, Hora de entrada: {row[3]}, Minutos de Entrada: {row[4]}, Hora de salida: {row[5]}, Minutos de salida: {row[6]}")
    if os.listdir(directorio):
        print("HISTORIAL DE USUARIO")
        for filename in os.listdir(directorio):        
            with open(directorio + "/" + filename, "r") as file:
                for line in file:
                    print(line)        
    else:
        print("NO HAY NADA QUE MOSTRAR ANDATE DE AQUI!!!!!!!!")

def menu_borrar():
    print("1. Borrar un archivo")
    print("2. Borrar todos los archivos")
    print("3. Salir")

def ver_usuario():
    cursor.execute("SELECT * FROM parqueo;")
    usuario = cursor.fetchall()
    for user in usuario:
        print(f"Usuario: {user[0]}")


def solicitar_entero_positivo(mensaje):
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

def solicitar_entero_positivo_borrar(mensaje):
    while True:
        entrada = input(mensaje)
        if entrada.isdigit():
            numero = int(entrada)
            if numero > 0 and numero < 4:
                return numero
            else:
                print("Error: El número debe ser mayor que 0 y menor que 4")
        else:
            print("Error: Solo se permiten números enteros positivos.")

def solicitar_mensaje_string(mensaje):
    while True:
        entrada = input(mensaje)
        if entrada.isalpha():  
            return entrada
        else:
            print("Error: Solo se permiten letras.")

def actualizar_salida_usuario(user, hora_out, minutos_out):
    print("Actualizando la hora de salida para el usuario...")
    cursor.execute("UPDATE parqueo SET hora_salida = %s, minutos_salida = %s WHERE Usuario = %s;", (hora_out, minutos_out, user))
    conn.commit()
    print("Hora de salida actualizada correctamente para el usuario:", user)

def decode_qr(image):    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    decoded_objects = pyzbar.decode(gray)
    qr_data_list = []  
    for obj in decoded_objects:
        
        points = obj.polygon
        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points
        n = len(hull)
        for j in range(0, n):
            cv2.line(image, hull[j], hull[(j + 1) % n], (0, 255, 0), 3)
        
        qr_data = obj.data.decode("utf-8")
        qr_data_list.append(qr_data)  

        cv2.putText(image, qr_data, (obj.rect.left, obj.rect.top), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
    return image, qr_data_list


opcion = 0
opcionu = 0
primera_hora = 15
hora_restante = 20
# directorio_qr = "E:/perez/Documentos/Cursos 2do. Semestre 2024/PROYECTOS DE COMPUTACION APLICADA A I.E. Seccion P/Tareas Proyectos/Corto/qr"
# directorio = "E:/perez/Documentos/Cursos 2do. Semestre 2024/PROYECTOS DE COMPUTACION APLICADA A I.E. Seccion P/Tareas Proyectos/Corto/facturas"
# directorio_database = "E:/perez/Documentos/Cursos 2do. Semestre 2024/PROYECTOS DE COMPUTACION APLICADA A I.E. Seccion P/Tareas Proyectos/Corto/database"

directorio_qr = "/home/emerson/Documentos/Tareas_Proyectos/Corto/qr"
directorio = "/home/emerson/Documentos/Tareas_Proyectos/Corto/facturas"
directorio_database = "/home/emerson/Documentos/Tareas_Proyectos/Corto/database"
date_time = time.strftime("%m/%d/%Y, %H:%M:%S")

while opcion != 5:
    menu()
    opcion = solicitar_entero_positivo("Ingrese una opcion: ")

    if opcion == 1:
        user = solicitar_mensaje_string("Ingrese el nombre del usuario: ")
        nit = solicitar_entero_positivo("Ingrese el nit: ")
        placa = input("Ingrese la placa del vehiculo: ")
        hora_in = int(time.strftime("%H", time.localtime()))
        minutos_in = int(time.strftime("%M", time.localtime()))
        hora_out = 0  
        minutos_out = 0
        total=0
        
        info_usuario(user, nit, placa, hora_in, minutos_in, hora_out, minutos_out)
        hora_qr = [hora_in, minutos_in]
        print(type(hora_qr))
        img = qrcode.make(hora_qr)
        f = open(f"{directorio_qr}/{user}.png", "wb")
        img.save(f)
        f.close()
        
        filename = os.path.join(directorio, f"{user}.txt")
        with open(filename, "w") as file:
            file.write("Bienvenido al Parqueo El COLOCHO\n")
            file.write(f"Usuario: {user.capitalize()}\n")
            file.write(f"Placa: {placa.upper()}\n")
            file.write(f"Nit: {nit}\n")
            file.write(f"Hora de entrada: {hora_in}:{minutos_in}\n")
            file.write(f"Hora de salida: {hora_out}:{minutos_out}\n")
            file.write(f"Total a pagar: Q. {round(total)}\n")
        
    elif opcion == 2:
        ver_usuario()

        readUserFile = solicitar_mensaje_string("Ingrese el nombre del usuario: ")
        hora_out = int(time.strftime("%H", time.localtime()))
        minutos_out = int(time.strftime("%M", time.localtime()))
        actualizar_salida_usuario(readUserFile,hora_out,minutos_out)
        cursor.execute("SELECT * FROM parqueo WHERE usuario = %s;", (readUserFile,))
        obtener_hora_in = cursor.fetchone()
        if actualizar_salida_usuario:
            placa = obtener_hora_in[2]
            nit = obtener_hora_in[1]
        print("Leyendo el coidgo QR...")
        image_path = directorio_qr + "/" + readUserFile + ".png"
        print(f"Ruta de la imagen: {image_path}") 
        image = cv2.imread(image_path)
        if image is None:
            print("Error: No se puede leer la imagen.")
        else:

            image, qr_data_list = decode_qr(image)

            for qr_data in qr_data_list:
                print("Datos del QR:", qr_data)
                print(type(qr_data))

            qr_data_list = ast.literal_eval(qr_data_list[0])

            if len(qr_data_list) == 2:
                hora_in = qr_data_list[0]
                minutos_in = qr_data_list[1]
            else:
                print("Error: No hay suficientes datos en el código QR.")    
        print(f"Su Hora de entrada fue: {hora_in}:{minutos_in} y su Hora de salida fue: {hora_out}:{minutos_out}")
        total_hora = ((hora_out - hora_in -1)*hora_restante) + primera_hora

        if minutos_out != 0 or minutos_in != 0:
            total_minutos = ((minutos_out - minutos_in)*hora_restante)/60
            round(total_minutos,2)
        if minutos_out == 0:
            total_minutos = ((minutos_in)*hora_restante)/60
            round(total_minutos,2)
        if hora_out == hora_in:
            total_hora = 0
            total_minutos = ((minutos_out - minutos_in)*primera_hora)/60
            round(total_minutos,2)
        if minutos_out < minutos_in and hora_out > hora_in:
            total_minutos = ((minutos_out + 60 - minutos_in)*hora_restante)/60
            round(total_minutos,2)
        if hora_out - hora_in == 1 and minutos_out < minutos_in:
            total_hora = 0
            total_minutos = ((minutos_out + 60 - minutos_in)*primera_hora)/60
            round(total_minutos,2)
        total = total_hora + total_minutos
        filename = os.path.join(directorio, f"{readUserFile}.txt")
        with open(filename, "w") as file:
            file.write("Bienvenido al Parqueo El COLOCHO\n")
            file.write(f"Usuario: {readUserFile.capitalize()}\n")
            file.write(f"Placa: {placa.upper()}\n")
            file.write(f"Nit: {nit}\n")
            file.write(f"Hora de entrada: {hora_in}:{minutos_in}\n")
            file.write(f"Hora de salida: {hora_out}:{minutos_out}\n")
            file.write(f"Total a pagar: Q. {round(total,2)}\n")
        filename = os.path.join(directorio, f"{readUserFile}.txt")
        try:
            with open(filename, 'r') as file:
                for line in file:
                    print(line.strip())
        except FileNotFoundError:
            print("El archivo no existe.")
        except Exception as e:
            print(f"Error al Leer el archivo: {e}")
        cv2.imshow("QR Code Scanner", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


        cursor.execute("SELECT * FROM parqueo;")
        rows = cursor.fetchall()
        for row in rows:
            print(f"Usuario: {row[0]}, Placa: {row[2]}, Nit: {row[1]}, Hora de entrada: {row[3]}, Minutos de Entrada: {row[4]}, Hora de salida: {row[5]}, Minutos de salida: {row[6]}")

    elif opcion == 3:
        menu_borrar()

        opcion = solicitar_entero_positivo_borrar("Ingrese una opción: ")
        if opcion == 1:
            ver_usuario()
            deleteUserFile = input('Ingrese el nombre del archivo a borrar: ')
            filename = os.path.join(directorio, deleteUserFile + '.txt')  
            filename_qr = os.path.join(directorio_qr, deleteUserFile + '.png')
            try:
                if os.path.exists(filename):
                    os.remove(filename)
                    cursor.execute("DELETE FROM parqueo WHERE usuario = %s;", (deleteUserFile,))
                    conn.commit()
                    print('Información borrada del archivo y usuario eliminado de la base de datos.')
                else:
                    print('Error: El archivo no existe.')
            except Exception as e:
                print('Error al borrar la información del archivo:', e)
        elif opcion == 2:
            for deletefile in os.listdir(directorio):
                dataname = deletefile.replace(".txt", "")
                cursor.execute("DELETE FROM parqueo WHERE usuario = %s;", (dataname,))
            conn.commit()
            print('Información de la base de datos eliminada')
    
            for deletefile in os.listdir(directorio):
                os.remove(os.path.join(directorio, deletefile))
            print('Todos los archivos han sido eliminados')
            for detelefileqr in os.listdir(directorio_qr):
                os.remove(os.path.join(directorio_qr, detelefileqr))
            print('Todos los archivos han sido eliminados')
        elif opcion == 3:
            print("Saliendo del Menu Borrar..")
    elif opcion == 4:
        historial()
    elif opcion == 5:
        print("Saliendo del programa...")
    else:
        print("Opción no válida, por favor intente de nuevo.")

cursor.close()
conn.close()
