import cv2 as cv
import os
import numpy as np

dataPath = '/home/emerson/Documentos/data_imagenes'
peopleList = os.listdir(dataPath)
dataModelEntrenamiento = '/home/emerson/Documentos/data_modelo_entrenamiento'
if not os.path.exists(dataModelEntrenamiento):
    print('Carpeta creada: ',dataModelEntrenamiento)
    os.makedirs(dataModelEntrenamiento)
print('Lista de personas: ', peopleList)

labes = []
facesData = []
label = 0

for nameDir in peopleList:
    personPath = dataPath + '/' + nameDir
    print('Leyendo las imágenes')

    for fileName in os.listdir(personPath):
        print('Rostros: ', nameDir + '/' + fileName)
        labes.append(label)
        facesData.append(cv.imread(personPath+'/'+fileName,0))
        image = cv.imread(personPath +'/'+fileName,0)
        cv.imshow('image',image)
        cv.waitKey(10)
    label = label + 1
print('labels= ',labes)
print('Número de etiquetas 0: ',np.count_nonzero(np.array(labes)==0))

#cv.destroyAllWindows()

face_recognizerEigenFace = cv.face.EigenFaceRecognizer_create()
print('Entrenando Modelo EingenFaceRecognizer...')
face_recognizerEigenFace.train(facesData, np.array(labes))   
face_recognizerEigenFace.write(dataModelEntrenamiento+'/modeloEigenFace.xml')
print('Modelo Almacenado en: ',dataModelEntrenamiento+'/modeloEigenFace.xml')
print("Modelo de Entrenamiento Termiando...")


face_recognizerLBPHFace= cv.face.LBPHFaceRecognizer_create()
print('Entrenando Modelo LBPHFaceRecognizer...')
face_recognizerLBPHFace.train(facesData, np.array(labes))
face_recognizerLBPHFace.write(dataModelEntrenamiento+'/modeloLBPHFace.xml')
print('Modelo Almacenado en: ',dataModelEntrenamiento+'/modeloLBPHFace.xml')
print("Modelo de Entrenamiento Termiando...")

# face_recognizerFisher= cv.face.FisherFaceRecognizer_create()
# print('Entrenando Modelo FisherRecognizer...')
# face_recognizerFisher.train(facesData, np.array(labes))
# face_recognizerFisher.write(dataModelEntrenamiento+'/modeloFisher.xml')
# print('Modelo Almacenado en: ',dataModelEntrenamiento+'/modeloFisher.xml')
# print("Modelo de Entrenamiento Termiando...")


