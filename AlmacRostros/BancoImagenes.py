import cv2 as cv
import os

imagesPath = "/home/emerson/Documentos/Banco_Imagenes"
imagesPathList = os.listdir(imagesPath)
print('imagesPathList =', imagesPathList)

if not os.path.exists('/home/emerson/Documentos/AlmacRostros'):
    print('Carpeta creada: AlmacRostros')
    os.makedirs('/home/emerson/Documentos/AlmacRostros')

faceClassif = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
count = 0

for imageName in imagesPathList:
    print('imageName =', imageName)
    image = cv.imread(imagesPath+'/'+imageName)
    imageAux = image.copy()
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    faces = faceClassif.detectMultiScale(gray, 1.1, 5)
    for (x,y,w,h) in faces:
        cv.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv.rectangle(image, (10, 5), (450, 25), (255, 255, 255), -1)
    cv.putText(image,'Presione S, para alamvenar los rostros encontadros',(10,20),2,0.5,(128,0,255,1),1,cv.LINE_AA)
    cv.imshow('image', image)
    k = cv.waitKey(0)
    if k == ord('s'):
        for (x,y,w,h) in faces:
            rostro = imageAux[y:y+h, x:x+w]
            rostro = cv.resize(rostro, (150, 150), interpolation=cv.INTER_CUBIC)
            cv.imwrite('/home/emerson/Documentos/AlmacRostros/Rostro_{}.jpg'.format(count), rostro)
            count = count + 1
    elif k == 27:
        break

cv.destroyAllWindows()