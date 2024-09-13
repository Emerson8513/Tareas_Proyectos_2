import cv2 as cv
import os

# Verifica si el directorio existe, si no, lo crea
if not os.path.exists('/home/emerson/Documentos/AlmacRostros'):
    print('Carpeta creada: AlmacRostros')
    os.makedirs('/home/emerson/Documentos/AlmacRostros')

# Captura de video
cap = cv.VideoCapture(0)
faceClassif = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
count = 0

while True:
    ret, frame = cap.read()
    frame = cv.flip(frame, 1)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    auxFrame = frame.copy()

    faces = faceClassif.detectMultiScale(gray, 1.1, 5) 
    k = cv.waitKey(1)
    if k == 27:  # Presiona Esc para salir
        break
    
    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        rostro = auxFrame[y:y+h, x:x+w]
        rostro = cv.resize(rostro, (150, 150), interpolation=cv.INTER_CUBIC)
        if k == ord('s'):  # Presiona 's' para guardar el rostro
            cv.imwrite('/home/emerson/Documentos/AlmacRostros/Rostro_{}.jpg'.format(count), rostro)
            count = count + 1
            cv.imshow('rostro', rostro)
    
    cv.rectangle(frame, (10, 5), (450, 25), (255, 255, 255), -1)
    cv.putText(frame, 'Presione s para almacenar rostros encontrados', (10, 20), 2, 0.5, (128, 0, 255), 1, cv.LINE_AA)
    cv.imshow('frame', frame)
    
cap.release()
cv.destroyAllWindows()
