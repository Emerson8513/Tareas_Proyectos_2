
db_name = "parqueo";
db_user = "postgres";
db_password = "kuto";
db_host = "localhost";
db_port = "5432";


create_table_query = {
    "CREATE TABLE IF NOT EXISTS parqueo ("...
    "Usuario VARCHAR(50), "...
    "nit int NOT NULL, "...
    "placa VARCHAR(50), "...
    "hora_entrada int NOT NULL, "...
    "minutos_entrada int NOT NULL, "...
    "hora_salida int NOT NULL, "...
    "minutos_salida int NOT NULL",...
    ");"
};
create_table_query_str = strjoin(create_table_query, "\n");


system(['psql -U ', db_user, ' -d ', db_name, ' -c "', create_table_query_str, '"']);

function info_usuario(user, nit, placa, hora_in, minutos_in, hora_out, minutos_out)
    printf("Bienvenido al Parqueo El COLOCHO\n");
    insert_query = sprintf('INSERT INTO parqueo (Usuario, nit, placa, hora_entrada, minutos_entrada, hora_salida, minutos_salida) VALUES (''%s'', %d, ''%s'', %d, %d, %d, %d);',
        user, nit, placa, hora_in, minutos_in, hora_out, minutos_out);
     system(['psql -U postgres -d parqueo -c "', insert_query, '"']);
endfunction

function menu()
    printf("QUE DESEA REALIZAR\n");
    printf("1. Ingresar Informacion de Usuario\n");
    printf("2. Ejecutar Programa\n");
    printf("3. Borrar Información\n");
    printf("4. Historial de Usuarios\n");
    printf("5. Salir\n");
endfunction
function menu_borrar()

    printf("1. Borrar un archivo\n")
    printf("2. Borrar todos los archivos\n")
    printf("3. Salir\n")
end

function historial()
    select_query = "SELECT * FROM parqueo;";
    system(['psql -U postgres -d parqueo -c "', select_query, '"']);
end

function ver_usuario()

endfunction
function numero = solicitar_entero_positivo(mensaje)
    while true
        entrada = input(mensaje, 's');
        if all(isstrprop(entrada, 'digit'))
            numero = str2num(entrada);
            if numero > 0
                break;
            else
                printf("Error: El número debe ser mayor que cero.\n");
            end
        else
            printf("Error: Solo se permiten números enteros positivos.\n");
        end
    end
end


function numero = solicitar_entero_no_negativo(mensaje)
    while true
        entrada = input(mensaje, 's');
        if !isempty(str2num(entrada))
            numero = str2num(entrada);
            if numero >= 0 && numero < 60
                return;
            else
                printf("Error: El número debe ser mayor o igual que cero y menor que 60.\n");
            endif
        else
            printf("Error: Solo se permiten números enteros positivos.\n");
        endif
    endwhile
endfunction

function numero = solicitar_entero_positivo_borrar(mensaje)
    while true
        entrada = input(mensaje, 's');
        if !isempty(str2num(entrada))
            numero = str2num(entrada);
            if numero > 0 && numero < 4
                return;
            else
                printf("Error: El número debe ser mayor que 0 y menor que 4\n");
            endif
        else
            printf("Error: Solo se permiten números enteros positivos.\n");
        endif
    endwhile
endfunction

function numero = solicitar_hora(mensaje)
    while true
        entrada = input(mensaje, 's');
        if !isempty(str2num(entrada))
            numero = str2num(entrada);
            if numero >= 0 && numero < 24
                return;
            else
                printf("Error: La hora debe ser mayor o igual que cero y menor que 24.\n");
            endif
        else
            printf("Error: Solo se permiten números enteros positivos.\n");
        endif
    endwhile
endfunction

function entrada = solicitar_mensaje_string(mensaje)

    while true
        entrada = input(mensaje, 's');
        if all(isletter(entrada))
            return;
        else
            disp("Error: Solo se permiten letras.");
        end
    end
end

opcion = 0;
opcionu = 0;
primera_hora = 15;
hora_restante = 20;
directorio = 'E:/perez/Documentos/Cursos 2do. Semestre 2024/PROYECTOS DE COMPUTACION APLICADA A I.E. Seccion P/Tareas Proyectos/Corto/facturas/';


while opcion != 5
    menu();
    opcion = solicitar_entero_positivo("Ingrese una opción: ");

    if opcion == 1
        user = solicitar_mensaje_string("Ingrese Nombre de Usuario: ");
        nit = solicitar_entero_positivo("Ingrese el nit: ");
        placa = input("Ingrese su placa: ", 's');
        hora_in = solicitar_hora("Ingrese la hora de entrada: ");
        minutos_in = solicitar_entero_no_negativo("Ingrese los Minutos: ");
        hora_out = solicitar_hora("Ingrese la hora de salida: ");
        while hora_out < hora_in
            disp("Hora de salida incorrecta");
            hora_out = solicitar_hora("Ingrese la hora de salida: ");
        endwhile
        minutos_out = solicitar_entero_no_negativo("Ingrese los Minutos: ");

        info_usuario(user, nit, placa, hora_in, minutos_in, hora_out, minutos_out);
        filename = strcat(directorio, user, ".txt");

        total_hora = ((hora_out - hora_in - 1) * hora_restante) + primera_hora;


        if minutos_out != 0 || minutos_in != 0
            total_minutos = ((minutos_out - minutos_in) * hora_restante) / 60;
        elseif minutos_out == 0
           total_minutos = (minutos_in * hora_restante) / 60;
        end
        if hora_out == hora_in
            total_hora = 0
            total_minutos = ((minutos_out - minutos_in)*primera_hora)/60;
        endif
        if minutos_out < minutos_in && hora_out > hora_in
            total_minutos = ((minutos_out +60 - minutos_in)*hora_restante)/60;
        endif

        if hora_out - hora_in ==1 && minutos_out < minutos_in
            total_hora =0
            total_minutos = ((minutos_out +60 - minutos_in )*primera_hora)/60
        endif


        total = total_hora + total_minutos;


        fprintf("Total a pagar: Q. %.2f\n", total);

        fid = fopen(filename, "w");
        if fid != -1
            fprintf(fid, "Bienvenido al Parqueo El COLOCHO\n");
            fprintf(fid, "Usuario: %s\n", upper(user));
            fprintf(fid, "Placa: %s\n", upper(placa));
            fprintf(fid, "Nit: %d\n", nit);
            fprintf(fid, "Hora de entrada: %d:%d\n", hora_in, minutos_in);
            fprintf(fid, "Hora de salida: %d:%d\n", hora_out, minutos_out);
            fprintf(fid, "Total a pagar: Q. %d\n", total);
            fclose(fid);
        else
            printf("Error al abrir el archivo para escribir.\n");
        end

    elseif opcion == 2
        historial();
        readUserFile = input('Ingrese el nombre del archivo a leer: ', 's');
        filename = strcat(directorio, readUserFile, '.txt');

        fid = fopen(filename, 'r');
        if fid != -1
            while ~feof(fid)
                line = fgetl(fid);
                disp(line);
            end
            fclose(fid);
        else
            printf('Error al leer el archivo: El archivo no existe.\n');
        end

    elseif opcion == 3
        menu_borrar();
        opcion_borrar = solicitar_entero_positivo_borrar('Ingrese una opción: ');

        if opcion_borrar == 1
           historial();
           deleteUserFile = input('Ingrese el nombre del archivo a borrar: ', 's');
            filename = strcat(directorio, deleteUserFile, '.txt');

           if exist(filename, 'file')
                delete(filename);
               delete_query = sprintf("DELETE FROM parqueo WHERE Usuario = '%s';", deleteUserFile);
               system(['psql -U postgres -d parqueo -c "', delete_query, '"']);
               printf('Información borrada del archivo y usuario eliminado de la base de datos.\n');
           else
               printf('Error: El archivo no existe.\n');
           end

        elseif opcion_borrar == 2
           archivos = dir(fullfile(directorio, '*.txt'));
            for i = 1:length(archivos)
                deletefile = archivos(i).name;
                dataname = strrep(deletefile, '.txt', '');
                delete_query = sprintf("DELETE FROM parqueo WHERE Usuario = '%s';", dataname);
                system(['psql -U postgres -d parqueo -c "', delete_query, '"']);
            end
            printf('Información de la base de datos eliminada\n');

            for i = 1:length(archivos)
                deletefile = archivos(i).name;
                delete(fullfile(directorio, deletefile));
            end
            printf('Todos los archivos han sido eliminados\n');

       elseif opcion_borrar == 3
            printf('Saliendo del Menu Borrar..\n');
       end


    elseif opcion == 4
        historial();

    elseif opcion == 5
        printf("Saliendo del programa...\n");

    else
        printf("Opción no válida, por favor intente de nuevo.\n");
    end
end


