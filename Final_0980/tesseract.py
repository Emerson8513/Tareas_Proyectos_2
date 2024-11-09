import cv2
import pytesseract
import datetime

# Establece la ruta al ejecutable de Tesseract si es necesario
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Ajusta esta ruta si es necesario

# Inicia la captura de video desde la cámara
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('http://192.168.1.99:4747/video')

while True:
    # Captura cada fotograma
    ret, frame = cap.read()
    if not ret:
        break

    # Mostrar el fotograma en una ventana
    cv2.imshow('Captura en vivo', frame)

    # Detecta si se presiona la tecla 's' para capturar una imagen y procesarla
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        # Genera un nombre único para la imagen usando la fecha y hora actual
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"captura_{timestamp}.png"

        # Guarda la imagen capturada
        cv2.imwrite(filename, frame)
        print(f"Imagen capturada y guardada como {filename}")

        # Procesa la imagen capturada con OCR

        # Convertir la imagen a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Aplicar un umbral adaptativo para mejorar la nitidez del texto
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 11, 2)

        # Aplicar una operación de dilatación y erosión para limpiar ruido pequeño
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # Realiza el OCR en la imagen procesada
        text = pytesseract.image_to_string(processed, config='--psm 6')
        print("Texto detectado en la imagen capturada:", text)

    # Presiona 'q' para salir del bucle
    elif key == ord('q'):
        break

# Libera los recursos
cap.release()
cv2.destroyAllWindows()
