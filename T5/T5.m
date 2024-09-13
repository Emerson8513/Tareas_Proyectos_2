pkg load database

conn = pq_connect(setdbopts("dbname", "imc", "host", "localhost", "port", "5432", "user", "postgres", "password", "kuto"));


%Ingresar
%nombre = 'Juan';
%peso = 75;
%altura = 180;

%insert_query = "INSERT INTO imc (nombre, peso, altura) VALUES ($1, $2, $3);";
%pq_exec_params(conn, insert_query, {nombre, peso, altura});


% Borrar un registro
%nombre = 'Juan';

%delete_query = "DELETE FROM imc WHERE nombre = $1;";
%pq_exec_params(conn, delete_query, {nombre});

%N = pq_exec_params(conn, 'select * from imc;');



% Actualizar el peso y altura de un registro
%nuevo_peso = 80;
%nueva_altura = 182;
%nombre = 'Juan';

%update_query = "UPDATE imc SET peso = $1, altura = $2 WHERE nombre = $3;";
%pq_exec_params(conn, update_query, {nuevo_peso, nueva_altura, nombre});

bajoPeso = "Bajo Peso";
pesoNormal = "Peso Normal";
sobrePeso = "Sobrepeso";
filename = 'E:/perez/Documentos/Cursos 2do. Semestre 2024/PROYECTOS DE COMPUTACION APLICADA A I.E. Sección P/Tareas Proyectos/imc.txt';

opcion = 0;
opcionu = 0;
while opcion ~= 5
  % Menú de Opciones
  disp('Seleccione una Opción: ')
  disp('1. Usuario')
  disp('2. Calcular IMC y Mostrar Resultados')
  disp('3. Leer Archivo')
  disp('4. Borrar Información')
  disp('5. Salir')
  opcion = input('Ingrese su Elección: ');

  switch opcion
    case 1
      try
        % Menú de Usuario
        while opcionu ~= 4
          disp('Seleccione una Opción: ')
          disp('1. Añadir Usuario')
          disp('2. Actualizar Usuario')
          disp('3. Borrar Usuario')
          disp('4. Salir')
          opcionu = input('Ingrese la Opción: ');

          switch opcionu
            case 1
              disp('Añadiendo usuario...');
              nombre = input('Ingrese el Nombre del Usuario: ', 's');
              altura = input('Ingrese la Altura del Usuario en CM: ');
              if altura <= 0
                while altura <= 0
                  disp("Altura No Validad")
                  altura = input('Ingrese La Altura del Usuario en CM: ');
                endwhile
              endif
              peso = input('Ingrese el Peso del Usuario en Libras: ');
              if peso <= 0
                while peso <= 0
                  disp('Peso no Valido')
                  peso = input('Ingrese el Peso del Usuario en Libras')
                endwhile
              endif

              insert_query = "INSERT INTO imc (nombre, peso, altura) VALUES ($1, $2, $3);";
              pq_exec_params(conn, insert_query, {nombre, peso, altura});
              disp('Usuario añadido...');

            case 2
              nombre = input('Ingrese el Nombre del Usuario: ', 's');
              altura = input('Actualizar Altura del Usuario en CM: ');
              if altura <= 0
                while altura <= 0
                  disp('Altura No Valida')
                  altura = input('Actualizar Altura del Usuario en CM: ');
                endwhile
              endif
              peso = input('Actualizar el Peso del Usuario en Libras: ');
              if peso <= 0
                while peso <= 0
                  disp('Peso no Valido')
                  peso = input('Actualizar el Peso del Usuario en Libras: ');
                endwhile
              endif
              update_query = "UPDATE imc SET peso = $1, altura = $2 WHERE nombre = $3;";
              pq_exec_params(conn, update_query, {peso, altura, nombre});
              disp('Usuario actualizado...');

            case 3
              nombre = input('Ingrese el Nombre del Usuario a Borrar: ', 's');
              delete_query = "DELETE FROM imc WHERE nombre = $1;";
              pq_exec_params(conn, delete_query, {nombre});
              disp('Usuario borrado...');

            case 4
              disp('Saliendo');

            otherwise
              disp('Opción no válida.');
          end
        end
      catch
        disp('Error al gestionar el usuario');
      end
    case 2
      try
        nombre_usuario = input('Ingrese el Nombre: ', 's');
        query = "SELECT peso, altura FROM imc WHERE nombre = $1;";
        result = pq_exec_params(conn, query, {nombre_usuario});

        % Mensajes de depuración
        disp('Resultado de la consulta:');
        disp(result);
        disp(['Tipo de resultado: ', class(result)]);

        if isempty(result) || isempty(result.data)
          disp('Usuario no encontrado o datos vacíos');
        else
          % Extraer los valores de peso y altura de la estructura
          try
            peso = result.data{1,1};   % El primer valor en la primera fila
            altura = result.data{1,2}; % El segundo valor en la primera fila

            if peso < 80
              estado = bajoPeso;
              disp(estado);
            elseif peso > 81 && peso < 150
              estado = pesoNormal;
              disp(estado);
            elseif peso > 151
              estado = sobrePeso;
              disp(estado);
            endif

            disp(['Peso extraído: ', num2str(peso)]);
            disp(['Altura extraída: ', num2str(altura)]);

            if isempty(peso) || isempty(altura) || peso <= 0 || altura <= 0
              disp('Error: Los valores de peso y altura son inválidos.');
            else
              imc = (peso * 0.453592) / ((altura / 100) ^ 2);
              disp(['Peso: ', num2str(peso)]);
              disp(['Altura: ', num2str(altura)]);
              disp(['IMC: ', num2str(imc)]);

              % Abrir archivo para escritura (vaciar archivo si ya existe)
              fileID = fopen(filename, 'w');
              if fileID == -1
                error('No se pudo abrir el archivo para escritura.');
              end
              fprintf(fileID, 'Usuario %s\n', nombre_usuario);
              fprintf(fileID, 'Peso: %.2f Libras\n', peso);
              fprintf(fileID, 'Altura: %.2f CM\n', altura);
              fprintf(fileID, 'IMC: %.2f\n', imc);
              fprintf(fileID, 'Estado: %s\n', estado);
              fclose(fileID);
            end
          catch
            disp('Error al extraer o convertir los datos');
          end
        end
      catch
        disp('Error al calcular y mostrar el IMC');
      end
    case 3
      try
        % Leer archivo
        fileIA = fopen(filename, 'r');
        if fileIA == -1
          error('No se pudo abrir el archivo para lectura.');
        endif
        while ~feof(fileIA)
          line = fgetl(fileIA);
          if ischar(line)
            disp(line);
          else
            disp('Error al leer una línea del archivo.');
          endif
        endwhile
        fclose(fileIA);
      catch
        disp('Error al leer el archivo');
      end
    case 4
      try
        % Borrar información del archivo
        fileID = fopen(filename, 'w');
        if fileID == -1
          error('No se pudo abrir el archivo para escritura.');
        end
        fclose(fileID);
        disp('Información borrada del archivo.');
      catch
        disp('Error al borrar la información del archivo');
      end
    case 5
      disp('Saliendo del Programa');
      disp('Gracias por usar el programa');
    otherwise
      disp('Opción no válida');
  end
end
