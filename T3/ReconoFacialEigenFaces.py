import cv2 as cv
import os



dataPath = '/home/emerson/Documentos/data_imagenes/' #Cambia a la ruta donde hayas almacenado Data
imagePaths = os.listdir(dataPath)
print('imagePaths=',imagePaths)

face_recognizer = cv.face.EigenFaceRecognizer_create()

# Leyendo el modelo
face_recognizer.read('/home/emerson/Documentos/data_modelo_entrenamiento/modeloEigenFace.xml')


#cap = cv.VideoCapture(0)
#cap = cv.VideoCapture('/home/emerson/Vídeos/my_video-1.mkv')
cap = cv.VideoCapture('/home/emerson/Vídeos/Ejemplo3.mp4')
faceClassif = cv.CascadeClassifier(cv.data.haarcascades+'haarcascade_frontalface_default.xml')

while True:
    ret,frame = cap.read()
    if ret == False: break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    auxFrame = gray.copy()

    faces = faceClassif.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:
        rostro = auxFrame[y:y+h,x:x+w]
        rostro = cv.resize(rostro,(150,150),interpolation= cv.INTER_CUBIC)
        result = face_recognizer.predict(rostro)

        cv.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv.LINE_AA)
        
        # EigenFaces
        if result[1] < 5700:
            cv.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv.LINE_AA)
            cv.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
        else:
            cv.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv.LINE_AA)
            cv.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
        

        
    cv.imshow('frame',frame)
    k = cv.waitKey(1)
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()