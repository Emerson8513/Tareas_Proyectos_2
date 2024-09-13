import cv2 as cv
import numpy as np

faceClassif = cv.CascadeClassifier('T3/haarcascade_frontalface_default.xml')

image = cv.imread('T3/personas.png')
imageAux = image.copy()
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

faces = faceClassif.detectMultiScale(gray, 1.1, 5)
count = 0

for (x, y, w, h) in faces:
    cv.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    rostro = imageAux[y:y+h, x:x+w]
    rostro = cv.resize(rostro, (150, 150), interpolation=cv.INTER_CUBIC)
    cv.imwrite('AlmacRostros/Rostro_{}.jpg'.format(count), rostro)
    count = count + 1
    cv.imshow('Rostro', rostro)
    cv.imshow('image', image)
    cv.waitKey(0)

cv.destroyAllWindows()
