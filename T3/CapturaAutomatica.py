import cv2 as cv
import os
import imutils

personName = 'Emerson'
dataPath = '/home/emerson/Documentos/data_imagenes'
personPath = dataPath + '/' + personName

if not os.path.exists(personPath):
    print('Carpeta creada: ',personPath)
    os.makedirs(personPath)

cap = cv.VideoCapture(0)
#cap = cv.VideoCapture('/home/emerson/Vídeos/my_video-1.mkv')

faceClassif = cv.CascadeClassifier(cv.data.haarcascades+'haarcascade_frontalface_default.xml')
count = 0

while True:
    
    ret, frame = cap.read()
    if ret == False: break
    frame =  imutils.resize(frame, width=640)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    auxFrame = frame.copy()

    faces = faceClassif.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:
        cv.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
        rostro = auxFrame[y:y+h,x:x+w]
        rostro = cv.resize(rostro,(150,150),interpolation=cv.INTER_CUBIC)
        cv.imwrite(personPath + '/rotro_{}.jpg'.format(count),rostro)
        count = count + 1
    cv.imshow('frame',frame)

    k =  cv.waitKey(1)
    if k == 27 or count >= 600:
        break

cap.release()
cv.destroyAllWindows()