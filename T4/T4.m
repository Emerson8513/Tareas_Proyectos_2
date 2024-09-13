% Comprobar si estamos ejecutando en MATLAB O GNU Octave
if (exist('OCTAVE_VERSION', 'builtin') ~= 0)
  % Estamos en Octave
  pkg load signal;
end

% Menú Principal
opcion = 0;
while opcion ~= 5
  % Menú de Opciones
  disp('Seleccione una Opción: ')
  disp('1. Grabar')
  disp('2. Reproducir')
  disp('3. Graficar')
  disp('4. Graficar Densidad')
  disp('5. Salir')
  opcion = input('Ingrese su Elección: ');

  switch opcion
    case 1
      % Grabar Audio
      try
        duracion = input('Ingrese la Duración de la grabación en segundos: ');
        disp('Comenzando la Grabación...');
        recObj = audiorecorder;
        recordblocking(recObj, duracion);
        disp('Grabación Finalizada');
        data = getaudiodata(recObj);
        audiowrite('audio_octave.wav', data, recObj.SampleRate);
        disp('Archivo de audio grabado correctamente.');
      catch
        disp('Error al grabar el audio');
      end
    case 2
      %Reproducir Audio
      try
        [data,fs] = audioread('audio_octave.wav');
        sound(data,fs);
      catch
        disp('Error al Reproducir el audio.');
      end
    case 3
      % Grafico de Audio
      try
        [data,fs] = audioread('audio_octave.wav');
        tiempo = linspace(0,length(data)/fs,length(data));
        plot(tiempo,data);
        xlabel('Tiempo (s)');
        ylabel('Amplitud');
        title('Grafico de Audio');
      catch
        disp('Error al graficar el audio');
      end
     case 4
      %Graficando espectro de frecuencia
      try
        disp('Graficando espectro de frecuencia.. ');
        [audio,Fs] = audioread('audio_octave.wav');
        N = length(audio);
        f = linspace(0,Fs/2,N/2+1);
        ventana = hann(N);
        Sxx = pwelch(audio,ventana,0,N,Fs);
        plot(f,10*log10(Sxx(1:N/2+1)));
        xlabel('Frecuencia (Hz)');
        ylabel('Densidad Espectral de Potencia (dB/Hz)');
        title('Espectro de Frecuencia de la señal grabada');
      catch
        disp('Error al graficar el audio');
      end
     case 5
      disp('Saliendo del Programa');
    otherwise
      disp('Opcion no Validad');

  endswitch
endwhile

