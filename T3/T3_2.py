import cv2 as cv
import numpy as np

faceClassif = cv.CascadeClassifier('T3/haarcascade_frontalface_default.xml')

image = cv.imread('T3/personas.png')
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

faces = faceClassif.detectMultiScale(gray,
	scaleFactor=1.1,
	minNeighbors=6,
	minSize=(5,5),
	maxSize=(400,400))

for (x,y,w,h) in faces:
	cv.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

cv.imshow('image',image)
cv.waitKey(0)
cv.destroyAllWindows()