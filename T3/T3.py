import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
face_reco = cv.CascadeClassifier('T3/haarcascade_frontalface_default.xml')

while True:
    ret,frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    faces = face_reco.detectMultiScale(gray, 1.3, 5)
    cv.imshow('Video', frame)
    for (x,y,w,h) in faces:
        cv.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
    
    cv.imshow('Reconocimiento', frame)
    if cv.waitKey(1) & 0xFF == ord('s'):
        break
cap.release()
cv.destroyAllWindows()