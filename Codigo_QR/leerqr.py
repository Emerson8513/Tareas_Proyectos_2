import cv2
from pyzbar import pyzbar
import numpy as np
import ast 
import os

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

# directorio_qr = "E:/perez/Documentos/Cursos 2do. Semestre 2024/PROYECTOS DE COMPUTACION APLICADA A I.E. Seccion P/Tareas Proyectos/Corto/qr"
directorio_qr = "/home/emerson/Documentos/Tareas_Proyectos/Corto/qr"
for i in os.listdir(directorio_qr):
    print(i)

image_path = input("Ingrese el nombre de la imagen con el código QR: ")

filename= directorio_qr + '/' + image_path + '.png'
print(filename)
image = cv2.imread(filename)
hora_restante = 20
primera_hora = 15
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

    print("Hora de entrada:", hora_in)
    print("Minutos de entrada:", minutos_in)


    # Mostrar la imagen con el código QR decodificado
    cv2.imshow("QR Code Scanner", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()