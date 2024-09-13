# sudo apt-get install portaudio19-dev
import pyaudio
import wave
import simpleaudio as sa
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.io.wavfile as wav

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

opcion = 0
audio = pyaudio.PyAudio()
while opcion != 5:
    opcion += 1
    print(" 1. Grabar Audio\n 2. Reproducir Audio\n 3. Graficar\n 4. Graficar Espectro de Audio\n 5. Salir")
    opcion = int(input("\n Seleccione una Opcion: "))

    if opcion == 1:
        timpo_audio = int(input("Ingrese la duracion de Audio en Segundos(s): "))
        name_audio = input("Ingrese el nombre del archivo de Audio: ")
        stream = audio.open(format=FORMAT, channels=CHANNELS,rate = RATE, input=True,frames_per_buffer=CHUNK)
        print("Comenzando la Grabacionde Audio...")
        frames = []
        for i in range(0, int(RATE / CHUNK * timpo_audio)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("Grabacion de Audio Finalizada...")

        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        with wave.open(name_audio, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            print(f"Archivo Guardado como: {name_audio}")

    elif opcion == 2:
        name_audio = input("Ingrese el nombre del archivo de Audio: ")
        wave_obj = sa.WaveObject.from_wave_file('/home/emerson/Documentos/Tareas_Proyectos'+'/'+name_audio)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    
    elif opcion == 3:
        print("Graficando Audio...")

        name_audio = input("Ingrese el nombre del archivo de Audio: ")
        wf = wave.open(name_audio, 'rb')
        data = wf.readframes(wf.getnframes())
        data = np.frombuffer(data, np.int16)
        plt.plot(data)
        plt.show()
        wf.close()

    elif opcion == 4:
        name_audio = input("Ingrese el nombre del archivo de Audio:")
        Fs,audio = wav.read(name_audio)
        print("Graficando Espectro de Audio...")
        Nw = len(audio)
        f = np.linspace(0,Fs/2,Nw//2+1)
        ventana= np.hanning(Nw)

        f,Sxx = signal.welch(audio,fs=Fs,window=ventana,nperseg=Nw,noverlap=Nw/2,nfft=Nw)

        plt.plot(f,10*np.log10(Sxx))
        plt.grid(True)
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Densidad de Potencia Espectral (dB/Hz)')
        plt.show()
    elif opcion == 5:
        print("Saliendo...")
        break

